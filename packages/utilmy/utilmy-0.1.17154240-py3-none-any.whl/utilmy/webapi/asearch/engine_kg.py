"""
  


#### Goal to small proptopye of KG retrieval


   A) Indexer :  Extract Triplet (A, relation, B) from raw text --> store in database/NebulaGraph
            Alot of connected keyword. : normalize keywords, extra triplets


   B) query  :
       query --> extract keyword from query --> search in KG datas using keyword and relation around keyword
            --> hybrid with emebdding  -->





####
  Groq Engine : Cloud service Host llama3, 
       very fast very cheap,  500 token/seconds,  Alternative to GPT 3.5  (cheaper/faster)

     



######################################################################################################
#### Entity Extractor :

   https://github.com/zjunlp/DeepKE

   https://github.com/thunlp/OpenNRE

   https://github.com/zjunlp/KnowLM

   https://maartengr.github.io/BERTopic/getting_started/representation/representation.html#maximalmarginalrelevance

   
   
1)
   Llamax -- use LLM + Prompt

2) BERt like model to extract.(faster/cheaper) 
  https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa

  pre-trained model.  --> with huggingFae directlyt.
       https://huggingface.co/Babelscape/mrebel-large


3) ... NER extraction...


 
Llama Index --> Nebula Graph




without LLM, one way:
https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa


####Groq is cheap/Fast for Llama3 Enitry extraction
    https://towardsdatascience.com/relation-extraction-with-llama3-models-f8bc41858b9e



#### Questions Pairs
    https://huggingface.co/datasets/databricks/databricks-dolly-15k



REBEL model

   https://huggingface.co/Babelscape/mrebel-large




Building the KG graph index is the trickier part....

   https://github.com/wenqiglantz/llamaindex_nebulagraph_phillies/tree/main

   https://towardsdatascience.com/12-rag-pain-points-and-proposed-solutions-43709939a28c



hacked the coedium engine to access by CLI (ie auto generate the docstring)


"""
import warnings

warnings.filterwarnings("ignore")
import os, pathlib, uuid, time, traceback
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
from box import Box  ## use dot notation as pseudo class

import pandas as pd, numpy as np, torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline


############################################
from utilmy import pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob
from utilmy import log, log2




def test0():
    triplet_extractor = pipeline('translation_xx_to_yy', model='Babelscape/mrebel-base', tokenizer='Babelscape/mrebel-base')


    # We need to use the tokenizer manually since we need special tokens.
    msg="The Red Hot Chili Peppers were formed in Los Angeles by Kiedis, Flea, guitarist Hillel Slovak and drummer Jack Irons."
    extracted_text = triplet_extractor.tokenizer.batch_decode([triplet_extractor(msg, 
        src_lang="en", return_tensors=True, return_text=False)[0]["translation_token_ids"]]) # change __en__ for the language of the source.
    print(extracted_text[0])




################################################################################
#     # Function to parse the generated text and extract the triplets
def extract_triplets_typed(text):
    triplets = []
    relation = ''
    text = text.strip()
    current = 'x'
    subject, relation, object_, object_type, subject_type = '','','','',''

    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").replace("tp_XX", "").replace("__en__", "").split():
        if token == "<triplet>" or token == "<relation>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(),'tail': object_.strip(), 'tail_type': object_type})
                relation = ''
            subject = ''
        elif token.startswith("<") and token.endswith(">"):
            if current == 't' or current == 'o':
                current = 's'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(),'tail': object_.strip(), 'tail_type': object_type})
                object_ = ''
                subject_type = token[1:-1]
            else:
                current = 'o'
                object_type = token[1:-1]
                relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '' and object_type != '' and subject_type != '':
        triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(),'tail': object_.strip(), 'tail_type': object_type})
    return triplets



class TripletExtractorModel:
    def __init__(self, model_id, model_type, device: str = "", embed_size: int = 128):
        self.model_id = model_id
        self.model_type = model_type

        self.device = torch_getdevice(device)

        if model_type == "mrebel":
            self.pipeline =  pipeline('translation_xx_to_yy', model='Babelscape/mrebel-base', tokenizer='Babelscape/mrebel-base')

        else:
            raise ValueError(f"Invalid model type: {model_type}")

    def extract(self, text_list:list):

        for texti in text_list:
        text2 = self.pipeline.tokenizer.batch_decode([triplet_extractor(text, 
                src_lang="en", return_tensors=True, return_text=False)[0]["translation_token_ids"]]) # change __en__ for the language of the source.
        print(text2[0])
        triplet = extract_triplets_typed(text2)
        return triplet_list



def kg_model_extract(dirin="myraw.csv", model="Babelscape/mrebel-base", dirout="export.csv", coltxt="text") :

   dfraw = pd_read_file(dirin) 
   txt_list= dfraw[coltxt]


   extractor = TripletExtractorModel()
   extracted_triplets = extractor.extract(txt_list)
   print(extracted_triplets)

   kg_relation_save(extracted_triplets, dirout="data/kg_relation.csv" ) 




def kg_relation_save(extracted_triplets, dirout="data/kg_relation.csv" ):

    df = pd.DataFrame(columns=['A', 'relation', 'B', "info_json"])
    df["info_json"] = json.dumps("{}")

    ### insert  triplets
    #for triplet in extracted_triplets :
    #    df = pd_append(df, [triplet["head"], triplet["type"], triplet["tail"], triplet["info_json"]])


    pd_to_file(df, dirout, show=1)


def kg_db_insert_triplet_file(dirin="data/kg_relation.csv", table="kg_relation") :
      """ Load

      """
      df = pd_read_file(dirin) 



      #### Insert Nebula Code Graph using LlamaIndex 



###################################################################################################
if __name__ == "__main__":
    import fire

    fire.Fire()









