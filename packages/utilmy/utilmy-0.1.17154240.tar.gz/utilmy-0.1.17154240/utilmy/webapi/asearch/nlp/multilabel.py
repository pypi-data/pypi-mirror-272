""" 
pip install fire utilmy


git clone 
git checkout devtorch

cd webapi/asearch/nlp
mkdir -p ztmp
python mutilabel.py run_train --device "cpu"




ttps://www.kaggle.com/datasets/spsayakpaul/arxiv-paper-abstracts

For label = "cs.ML"
   Cat1 : cs
   Cat2:  ML



"""
import os
import pandas as pd
from transformers import DebertaTokenizer, DebertaForSequenceClassification, Trainer, TrainingArguments, TrainerCallback
import torch
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from datasets import Dataset
from sklearn.model_selection import train_test_split
from collections import Counter



from transformers import DebertaTokenizer, DebertaForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import torch
import numpy as np

from utilmy import pd_read_file


def data_normalize(df):
    """  Create custom category from raw label
        ['cs.CV', 'cs.AI', 'cs.LG']

    """ 
    df["label2"] = df["term"].apply(lambda x:  sorted(x.split(",")) )  # ['cs.CV', 'cs.AI', 'cs.LG']

    df["cat1"] = df["label2"].apply(lambda x: x[0].split(".")[0])  # "cs"
    df["cat2"] = df["label2"].apply(lambda x: x[0].split(".")[1])  # "CV"

    df["cat3"] = df["label2"].apply(lambda x: x[1].split(".")[0])  # "cs"
    df["cat4"] = df["label2"].apply(lambda x: x[1].split(".")[1])  # "AI"


    return df 






def data_prepro(dirin= '.ztmp/arxiv_data.csv'):
    # Load dataset
    df = pd.read_csv(dirin)
    df = df.head(200)  # Select only the first 1000 rows

    # Preprocess data: Create custom category columns
    #df['categories_list'] = df['terms'].apply(lambda x: x.split(','))

    df["label2"] = df["terms"].apply(lambda x:  sorted(x.split(",")) )  # ['cs.CV', 'cs.AI', 'cs.LG']

    df["cat1"] = df["label2"].apply(lambda x: x[0].split(".")[0])  # "cs"
    df["cat2"] = df["label2"].apply(lambda x: x[0].split(".")[1])  # "CV"

    df["cat3"] = df["label2"].apply(lambda x: x[1].split(".")[0] if len(x)>1 else "NA" )  # "cs"
    df["cat4"] = df["label2"].apply(lambda x: x[1].split(".")[1] if len(x)>1 else "NA" )  # "AI"

    mlb = MultiLabelBinarizer()
    cat1 = mlb.fit_transform(df['cat1'].tolist())
    cat2 = mlb.fit_transform(df['cat2'].tolist())
    cat3 = mlb.fit_transform(df['cat3'].tolist())
    cat4 = mlb.fit_transform(df['cat4'].tolist())


    # Convert DataFrame to a dictionary
    data = {'summaries': df['summaries'].tolist(), 'cat1': cat1.tolist() , 'cat2': cat2.tolist() ,
            'labels3': cat3.tolist() , 'cat4': cat4.tolist()             
           }
   
    return data 


def data_tokenize_split(data):
    # Tokenization
    tokenizer = DebertaTokenizer.from_pretrained('microsoft/deberta-base')

    def preprocess_function(examples):
        output = tokenizer(examples['summaries'], truncation=True, padding=True, max_length=128)
        output['input_ids'] = output.pop('input_ids')  # Add input_ids to the output
        return output

    # Load the dataset
    dataset = Dataset.from_dict(data)

    # Encode texts
    dataset = dataset.map(preprocess_function, batched=True)

    # Remove labels with only a single instance
    label_counts = Counter([tuple(label) for label in dataset['cat1']])
    valid_labels = [label for label, count in label_counts.items() if count > 1]
    dataset      = dataset.filter(lambda example: tuple(example['cat1']) in valid_labels)

    # Split dataset into training and validation sets with stratification
    summaries_train, summaries_test, labels_train, labels_test = train_test_split(
        dataset['summaries'], dataset['labels'], 
        test_size=0.2, random_state=42, stratify=dataset['labels']
    )

    train_dataset = Dataset.from_dict({'summaries': summaries_train, 'labels': labels_train, 'input_ids': dataset['input_ids'][:len(summaries_train)]})
    test_dataset  = Dataset.from_dict({'summaries': summaries_test, 'labels': labels_test, 'input_ids': dataset['input_ids'][len(summaries_train):]})
    return train_dataset, test_dataset



def run_train(device="cpu"):

    model_id= 'microsoft/deberta-base'
    # Set device to CPU
    device = torch.device(device)

    # Load data
    data = data_prepro()
    train_dataset, test_dataset = data_tokenize_split(data)

   
    # Load model and move to CPU
    model = DebertaForSequenceClassification.from_pretrained(model_id, num_labels=len(mlb.classes_))
    model.to(device)

    # Collect loss and f1-score for plotting
    losses = []
    f1_scores = []

    # Define TrainingArguments
    training_args = TrainingArguments(
        output_dir='./results',
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=10,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
    )


    # Custom callback to log losses and f1-scores
    class CustomCallback(TrainerCallback):
        def on_log(self, args, state, control, logs=None, **kwargs):
            if logs is not None:
                losses.append(logs.get("eval_loss", 0.0))
                f1_scores.append(logs.get("eval_f1", 0.0))

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
        callbacks=[CustomCallback()]
    )

    # Train the model
    trainer.train()

    # Save the model and tokenizer
    model.save_pretrained('./deberta_finetuned')
    tokenizer.save_pretrained('./deberta_finetuned')
    model.to('cpu')  # Ensure the model is on CPU



def run_eval(dirmodel):

     model = load(dirmodel)

    # Inference example
    model.eval()
    test_texts = [example['summaries'] for example in test_dataset]
    predicted_categories = []

    for text in test_texts:
        encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
        encoded_input['input_ids'] = encoded_input.pop('input_ids')  # Add input_ids to the encoded_input
        encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
        output = model(**encoded_input)
        predictions = torch.sigmoid(output.logits).squeeze().detach().numpy()
        top_N = 3  # Change this to 4 or any other number you want
        top_labels = np.argsort(predictions)[-top_N:]  # Get the top N labels
        predicted_labels = [mlb.classes_[i] for i in top_labels]  # Get the corresponding labels
        predicted_categories.append(predicted_labels)


    # Print abstracts with predicted labels
    for abstract, labels in zip(test_texts, predicted_categories):
        print(f"Abstract: {abstract}\nPredicted Labels: {labels}\n")



# Custom metric for evaluation
def compute_metrics(eval_pred):
    logits = eval_pred.predictions
    labels = eval_pred.label_ids
    predictions = (torch.sigmoid(torch.Tensor(logits)) > 0.5).int()
    f1 = f1_score(torch.Tensor(labels).int().cpu().numpy(), predictions.cpu().numpy(), average='samples')
    return {"f1": f1}






###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()






def zz_run_train():
    # Load dataset
    # dataset = load_dataset('your_dataset_name')

    df = pd_read_file('ztmp/data.csv', sep="\t")

    # Preprocess data
    tokenizer = DebertaTokenizer.from_pretrained('microsoft/deberta-base')

    def preprocess_function(examples):
        return tokenizer(examples['text'], truncation=True, padding=True, max_length=128)

    encoded_dataset = dataset.map(preprocess_function, batched=True)

    # Model
    model = DebertaForSequenceClassification.from_pretrained('microsoft/deberta-base', num_labels=your_num_labels)

    # Define multi-label accuracy metric
    def multi_label_accuracy(preds, labels):
        sigmoid = torch.sigmoid(torch.Tensor(preds))
        threshold = torch.Tensor([0.5])
        predictions = (sigmoid > threshold).int()
        accuracy = (predictions == torch.Tensor(labels).int()).float().mean()
        return {"accuracy": accuracy.item()}

    # Training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded_dataset['train'],
        eval_dataset=encoded_dataset['test'],
        compute_metrics=multi_label_accuracy
    )

    # Train the model
    trainer.train()



    # Save the model
    model.save_pretrained('path/to/save/model')
    tokenizer.save_pretrained('path/to/save/tokenizer')

    # Reload the model
    from transformers import DebertaForSequenceClassification, DebertaTokenizer

    model = DebertaForSequenceClassification.from_pretrained('path/to/save/model')
    tokenizer = DebertaTokenizer.from_pretrained('path/to/save/tokenizer')


