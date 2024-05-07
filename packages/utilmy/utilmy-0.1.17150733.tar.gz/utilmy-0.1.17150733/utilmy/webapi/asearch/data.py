# -- coding: utf-8 --
"""
    #### Install
        cd myutil 
        cd utilmy/webapi/asearch/
        pip install -r pip/py39_full.txt
        pip install fastembed==0.2.6 loguru --no-deps


    #### ENV variables
        export HF_TOKEN=
]

    ##### Usage : 
            cd utilmy/webapi/asearch/
            mkdir -p ./ztmp

            python data.py run_convert --name "ag_news"  --diroot  "./ztmp/hf_datasets/"   

            to run for ashraq/financial-news-articles
            python data.py run_convert --name "ashraq/financial-news-articles" --diroot "./hf_datasets" --schema_fun "schema_ashraq_financial_news_articles"



    ##### Flow
        HFace Or Kaggle --> dataset in RAM--> parquet (ie same columns)  -->  parquet new columns (final)
        Example :   
             huggingface.co/datasets/valurank/News_Articles_Categorization
             {name}-{dataset_name}

              ### MetaData JSON saved here
                       ---> ztmp/hf_data/meta/valurank-News_Articles_Categorization.json"

              ### Data saved here:
                       ---> ztmp/hf_data/data/valurank-News_Articles_Categorization/train/df.parquet"
                       ---> ztmp/hf_data/data/valurank-News_Articles_Categorization/test/df.parquet"



       Target Schema is  SCHEMA_GLOBAL_v1 



    #### Dataset TODO:

        https://huggingface.co/datasets/ashraq/financial-news-articles

        https://huggingface.co/datasets/big_patent

        https://huggingface.co/datasets/cnn_dailymail



    ### Dataset Done
        https://huggingface.co/datasets/ag_news


    #### Dataset Done in Google Drtice
       https://drive.google.com/drive/folders/1Ggzl--7v8xUhxr8a8zpRtgh2fI9EXxoG?usp=sharing



    ##### Infos
        https://huggingface.co/datasets/big_patent/tree/refs%2Fconvert%2Fparquet/a/partial-train

        https://zenn.dev/kun432/scraps/1356729a3608d6




"""
import warnings
warnings.filterwarnings("ignore")
import os, pathlib, uuid, time, traceback, copy, json
from box import (Box, BoxList,  )
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
import pandas as pd, numpy as np, torch
import mmh3
from datasets import load_dataset
import datasets

from utilmy import pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob
from utilmy import log, log2


######################################################################################
#### All dataset has normalized columns : simplify training
SCHEMA_GLOBAL_v1 = [
    ("id_global",  "int64", "global unique ID"),
    ("id_dataset", "int64", "global unique ID of the dataset"),

    ("id_local", "int64", "local ID"),
    ("dt", "float64", "Unix timestamps"),

    ("title", "str", " Title "),
    ("summary", "str", " Summary "),
    ("body", "str", " Summary "),
    ("info_json", "str", " Extra info in JSON string format "),

    ("cat1", "str", " Category 1 or label "),
    ("cat2", "str", " Category 2 or label "),
    ("cat3", "str", " Category 3 or label "),
    ("cat4", "str", " Category 4 or label "),
    ("cat5", "str", " Category 5 or label "),
]



#### JSON saved on in  dirdata_meta/
meta_json =Box({
  "name"             : "str",
  "name_unique"      : "str",
  "url"              : "str",
  "nrows"            : "int64",
  "columns"          : "list",
  "columns_computed" : "list",  ### Computed columns from original
  "lang"             : "list",  ## list of languages
  "description_full" : "str",
  "description_short": "str",
  "tasks"            : "list",  ## List of tasks
  "info_json"        : "str",   ## JSON String to store more infos
  "dt_update"        : "int64", ## unix

})


####################################################################################
def run_convert(name="ashraq/financial-news-articles", diroot: str = "/content/drive/MyDrive/hf_dataset", schema_fun: str = "schema_ashraq_financial_news_articles"):
    """Converts the specified dataset to Parquet files."""
    # Load the dataset
    print("###### Loading dataset ")
    dataset = load_dataset(name)

    # Get the list of split names
    splits = list(dataset.keys())

    for key in splits:
        # Get the DataFrame for the current split
        df = pd.DataFrame(dataset[key])

        # Use the specified schema function for preprocessing the dataset
        convert_fun = globals()[schema_fun]
        df = convert_fun(df)

        # Print DataFrame information
        print(list(df.columns), df.shape)

        # Save DataFrame to Parquet file
        dirout = f"{diroot}/{name}/{key}/df.parquet"
        pd_to_file(df, dirout, show=1)

        # Generate metadata
        meta_dict = generate_metadata(df, name, key)
        # Save metadata dictionary as a JSON file
        json_save(meta_dict, f"{diroot}/meta/{name}-{key}.json")





def box_to_dict(box_obj):

    from box import (Box, BoxList,  )
    if isinstance(box_obj, Box):
        box_obj = {k: box_to_dict(v) for k, v in box_obj.items()}

    elif isinstance(box_obj, dict):
        return {k: box_to_dict(v) for k, v in box_obj.items()}
    elif isinstance(box_obj, list):
        return [box_to_dict(v) for v in box_obj]

    return str(box_obj) 


def hf_dataset_meta_todict(dataset):
   metadata = { "split": [] } 
   for split in dataset.keys():  ### Train
      ##### Convert metadata to dictionary
      mdict = {key: value for key, value in dataset[split].info._dict_.items()}
      metadata[split] = mdict
      metadata["split"].append(split)

   return metadata   





#######################################################################################
######## Custom Schema ################################################################
def hash_mmh64(xstr: str) -> int:
    # pylint: disable=E1136
    return mmh3.hash64(str(xstr), signed=False)[0]


def schema_agnews(df: pd.DataFrame, meta_dict: dict = None) -> pd.DataFrame:
    """Convert columns/ schema output a dataset for the ag_news dataset"""
    cols0 = ["text", "label"]
    log(df[cols0].shape)

    # Check if meta_dict is provided
    if meta_dict is None:
        log("No metadata provided. Using default values.")
        url = "https://huggingface.co/datasets/ag_news"
    else:
        url = meta_dict.get("url", "https://huggingface.co/datasets/ag_news")

    #### Taget columns
    n = len(df)
    dtunix = float(date_now(returnval="unix"))
    dataset_idhash  =  hash_mmh64(url) 

    df["id_global"]  = [uuid_int64() for i in range(n)]
    df["id_dataset"] = dataset_idhash
    df["dt"] = dtunix




    ###### Custom mapping ###########################
    df["id_local"]  = -1
    df["title"]     = df["text"].apply(lambda x: " ".join(x.split(" ")[:7]) )
    df["summary"]   = ""
    df["body"]      = df["text"]  ; del df["text"]
    df["info_json"] = df.apply(lambda x: json.dumps({}), axis=1)
    df["cat1"]      = df["label"] ; del df["label"]
    df["cat2"]      = ""
    df["cat3"]      = ""
    df["cat4"]      = ""
    df["cat5"]      = ""

    cols1 = [x[0] for x in  SCHEMA_GLOBAL_v1 ] 
    df = df[cols1]
    return df

def schema_ashraq_financial_news_articles(df: pd.DataFrame, meta_dict: dict = None) -> pd.DataFrame:
    """Preprocesses the Ashraq financial news articles dataset."""
    # Make a deep copy of the input DataFrame
    df_processed = df.copy()

    # Perform the preprocessing steps for the Ashraq dataset
    # For example, renaming columns, mapping categories, etc.
    df_processed.rename(columns={"title": "title", "text": "body", "label": "cat1"}, inplace=True)
    df_processed["summary"] = ""  # Add a summary column
    df_processed["info_json"] = df_processed.apply(lambda x: json.dumps({}), axis=1)  # Add an info_json column
    df_processed["cat2"] = ""  # Add cat2 column
    df_processed["cat3"] = ""  # Add cat3 column
    df_processed["cat4"] = ""  # Add cat4 column
    df_processed["cat5"] = ""  # Add cat5 column

    return df_processed

def uuid_int64():
    """## 64 bits integer UUID : global unique"""
    return uuid.uuid4().int & ((1 << 64) - 1)

def pd_to_file_split(df, dirout, ksize=1000):
    kmax = int(len(df) // ksize) + 1
    for k in range(0, kmax):
        log(k, ksize)
        dirouk = f"{dirout}/df_{k}.parquet"
        pd_to_file(df.iloc[k * ksize : (k + 1) * ksize, :], dirouk, show=0)

def np_str(v):
    return np.array([str(xi) for xi in v])

def pd_fake_data(nrows=1000, dirout=None, overwrite=False, reuse=True) -> pd.DataFrame:
    from faker import Faker

    if os.path.exists(str(dirout)) and reuse:
        log("Loading from disk")
        df = pd_read_file(dirout)
        return df

    fake = Faker()
    dtunix = date_now(returnval="unix")
    df = pd.DataFrame()

    ##### id is integer64bits
    df["id"] = [uuid_int64() for i in range(nrows)]
    df["dt"] = [int(dtunix) for i in range(nrows)]

    df["title"] = [fake.name() for i in range(nrows)]
    df["body"] = [fake.text() for i in range(nrows)]
    df["cat1"] = np_str(np.random.randint(0, 10, nrows))
    df["cat2"] = np_str(np.random.randint(0, 50, nrows))
    df["cat3"] = np_str(np.random.randint(0, 100, nrows))
    df["cat4"] = np_str(np.random.randint(0, 200, nrows))
    df["cat5"] = np_str(np.random.randint(0, 500, nrows))

    if dirout is not None:
        if not os.path.exists(dirout) or overwrite:
            pd_to_file(df, dirout, show=1)

    log(df.head(1), df.shape)
    return df

def pd_fake_data_batch(nrows=1000, dirout=None, nfile=1, overwrite=False) -> None:
    """Generate a batch of fake data and save it to Parquet files.

    python engine.py  pd_fake_data_batch --nrows 100000  dirout='ztmp/files/'  --nfile 10

    """

    for i in range(0, nfile):
        dirouti = f"{dirout}/df_text_{i}.parquet"
        pd_fake_data(nrows=nrows, dirout=dirouti, overwrite=overwrite)

def json_save(data, filename):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if it doesn't exist
    with open(filename, 'w') as f:
        json.dump(data, f, default=str)  # Use default=str to serialize non-serializable objects as strings

def generate_metadata(df, dataset_name, split_name):
    """Generate metadata based on the DataFrame."""
    meta_dict = {}

    # Extract features from DataFrame columns
    features = {column: {"dtype": str(df[column].dtype), "id": None} for column in df.columns}
    meta_dict["features"] = features

    # Other metadata attributes
    meta_dict["builder_name"] = "parquet"
    meta_dict["dataset_name"] = dataset_name
    meta_dict["config_name"] = "default"
    meta_dict["version"] = "0.0.0"
    meta_dict["download_size"] = None  # Add download size if available
    meta_dict["dataset_size"] = df.memory_usage(deep=True).sum()
    meta_dict["size_in_bytes"] = meta_dict["dataset_size"]

    # Calculate the number of examples and shard lengths
    num_examples = len(df)
    shard_lengths = [num_examples]
    meta_dict["splits"] = {split_name: {
        "name": split_name,
        "num_bytes": meta_dict["dataset_size"],
        "num_examples": num_examples,
        "shard_lengths": shard_lengths,
        "dataset_name": dataset_name
    }}

    return meta_dict

###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



