""" 
    ### Install
    pip intall gliner utilmy fire

    ### Usage
    cd asearch/
    export cfg="config/near/ner_cfg.yaml"

    python nlp/ner_gliner.py data_to_json  --cfg $cfg  --dirout ztmp/models/gliner/mymodel/

    python nlp/ner_gliner.py run_train     --cfg $cfg  --dirout ztmp/exp/
    
    python nlp/ner_gliner.py run_predict   --cfg $cfg  --dirout ztmp/models/gliner/mymodel/



"""
import os, json
from types import SimpleNamespace
from box import Box

from gliner import GLiNER
import torch
from transformers import get_cosine_schedule_with_warmup

from utilmy import (pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob, config_load,
                    json_save, json_load)
from utilmy import log, log2



##########################################################################################################
CONFIG_DEFAULT = Box(
        num_steps        = 4,  # number of training iteration
        train_batch_size = 2,
        eval_every       = 4 // 2,   # evaluation/saving steps
        save_directory   = "ztmp/exp/ztest/gliner/", # where to save checkpoints
        warmup_ratio     = 0.1,    # warmup steps
        device           = "cpu",
        lr_encoder       = 1e-5,   # learning rate for backbone
        lr_others        = 5e-5,   # learning rate for other parameters
        freeze_token_rep = False,  # freeze of not backbone
        
        # Parameters for set_sampling_params
        max_types          = 25,   # maximum number of entity types during training
        shuffle_types      = True, # if shuffle or not entity types
        random_drop        = True, # randomly drop entity types
        max_neg_type_ratio = 1,    # ratio of positive/negative types, 1 mean 50%/50%, 2 mean 33%/66%, 3 mean 25%/75% ...
        max_len            = 384   # maximum sentence length
  )



##########################################################################################################
def test1():
   pass

def data_to_json(cfg=None, dirin="ztmp/data.csv", dirout="ztmp/data/ner/sample_data.json"):
  """ Convert data to json 
  Input : csv or parquet file

  Target Frormat
  [
  {
    "tokenized_text": ["State", "University", "of", "New", "York", "Press", ",", "1997", "."],
    "ner": [ [ 0, 5, "Publisher" ] ]
  },
  
  """
  cfg = config_load(cfg)

  df = pd_read_file(dirin)

  #df["tokenized_text"] = df["text"].apply(lambda x: x.split())
  # 
 

  data= df[[ "tokenized_text", "ner"]].to_json(dirout, orient="records")
  log(str(data)[:100])
  json_save(data, dirout)



##########################################################################################################
def run_train(cfg:dict=None, cfg_name:str=None, dirout:str="ztmp/exp", 
              model_name:str="urchade/gliner_small",
              dirdata="ddata/sample_data.json"):
  """A function to train a model using specified configuration and data.
  Parameters:
      cfg (dict): Configuration dictionary (default is None).
      dirout (str): Output directory path (default is None).
      model_name (str): Name of model to use (default is "urchade/gliner_small").
      dirdata (str): Directory path of data to use (default is "data/sample_data.json").

  Returns:
      None
  """
  dt      = date_now(fmt="%Y%m%d/%H%M%S")
  device  = "cpu"
  dirout2 = f"{dirout}/{dt}"


  cfg    = config_load(cfg)
  config = cfg.get(cfg_name, None) if isinstance(cfg, dict) else None
  if config is None:
    config = CONFIG_DEFAULT
    nsteps = 2
    config.num_steps      = nsteps
    config.save_directory = dirout2
    config.eval_every     = nsteps // 2
    config.device         = device
    

  #### evaluation only support fix entity types (but can be easily extended)
  data  = json_load(dirdata)
  eval_data = {
      "entity_types": ["Person", 'Event Reservation'],
      "samples": data[:10]
  }


  log("##### Model Load", model_name)
  #### available models: https://huggingface.co/urchade
  model = GLiNER.from_pretrained(model_name)


  log("##### Train start")
  train(model, config, data, eval_data)

  dirfinal = f"{dirout2}/final/"
  log("##### Model Save", dirfinal)
  os_makedirs(dirfinal) 
  model.save_pretrained( dirfinal)




def run_predict(cfg:dict=None, dirmodel="ztmp/models/gliner/small", dirdata="ztmp/data/text.csv",
                dirout="ztmp/data/ner/predict/",
                kbatch=100):
  """Function to run prediction using a pre-trained GLiNER model.

    predict_entities(self, text, labels, flat_ner=True, threshold=0.5, multi_label=False):

  Parameters:
      cfg (dict): Configuration dictionary (default is None).
      dirmodel (str): Directory path of pre-trained model (default is "ztmp/models/gliner/small").
      dirdata (str): Directory path of input data (default is "ztmp/data/text.csv").

  #log(model.predict("My name is John Doe and I love my car. I bought a new car in 2020."))

  """
  model = GLiNER.from_pretrained(dirmodel, local_files_only=True)
  log(model)
  model.eval()

  df = pd_read_file(dirdata)
  log(df["text"].shape)

  df["ner"] = df["text"].apply(lambda x: model.predict(x))
  pd_to_file(df, dirout +"/df_predict_ner.parquet", show=1)



##########################################################################################################
def train(model, config, train_data, eval_data=None):

    cc = Box({})
    cc.config = dict(config)

    model = model.to(config.device)

    # Set sampling parameters from config
    model.set_sampling_params(
        max_types=config.max_types, 
        shuffle_types=config.shuffle_types, 
        random_drop=config.random_drop, 
        max_neg_type_ratio=config.max_neg_type_ratio, 
        max_len=config.max_len
    )
    
    model.train()

    train_loader = model.create_dataloader(train_data, batch_size=config.train_batch_size, shuffle=True)
    optimizer    = model.get_optimizer(config.lr_encoder, config.lr_others, config.freeze_token_rep)

    n_warmup_steps = int(config.num_steps * config.warmup_ratio) if config.warmup_ratio < 1 else  int(config.warmup_ratio)


    scheduler = get_cosine_schedule_with_warmup(optimizer,
        num_warmup_steps=n_warmup_steps,
        num_training_steps=config.num_steps)

    iter_train_loader = iter(train_loader)

    log("###### training Start Epoch...")
    for step in range(0, config.num_steps):
        try:
            x = next(iter_train_loader)
        except StopIteration:
            iter_train_loader = iter(train_loader)
            x = next(iter_train_loader)

        for k, v in x.items():
            if isinstance(v, torch.Tensor):
                x[k] = v.to(config.device)

        loss = model(x)  # Forward pass
            
        # Check if loss is nan
        if torch.isnan(loss):
            continue

        loss.backward()        # Compute gradients
        optimizer.step()       # Update parameters
        scheduler.step()       # Update learning rate schedule
        optimizer.zero_grad()  # Reset gradients

        descrip = f"step: {step} | epoch: {step // len(train_loader)} | loss: {loss.item():.2f}"
        log(descrip)

        if (step + 1) % config.eval_every == 0:
            model.eval()            
            if eval_data is not None:
                results, f1 = model.evaluate(eval_data["samples"], flat_ner=True, threshold=0.5,
                                      batch_size=12,
                                      entity_types=eval_data["entity_types"])

                log(f"Step={step}\n{results}")


            dirout2 = f"{config.save_directory}/finetuned_{step}"
            os_makedirs(dirout2)                
            model.save_pretrained(dirout2)
            #json_save(cc.to_dict(), f"{config.save_directory}/config.json")
            model.train()


###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



