import json

from scraper.src.db import MongoDatabase
from tqdm import tqdm
import subprocess

DATASET_SAVEPATH = '../data/'


def execute_bash_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error


def prepare_dataset():
    """Prepare dataset for finetuning.

    Struct (JSONL):
    {"prompt": "<prompt text>", "completion": "<ideal generated text>"}\n
    ...
    """
    db = MongoDatabase()
    dataset = []
    for query in tqdm(db.get_n_queries(-1)):
        prompt = query['label']
        completion = query['query']
        datapoint = {
            'prompt': prompt,
            'completion': ' ' + completion
        }
        dataset.append(datapoint)

    with open(DATASET_SAVEPATH + 'finetune_dataset.jsonl', 'w') as fd:
        for datapoint in dataset:
            fd.write(json.dumps(datapoint) + '\n')


# def validate_dataset():
#     val_cmd = f' {DATASET_SAVEPATH + "finetune_dataset.jsonl"}'
#     return execute_bash_command(val_cmd)


# def run_inference():
#     """Run inference on a dataset."""
#     inference_cmd = f'openai api fine_tunes.create -t {DATASET_SAVEPATH + "finetune_dataset.jsonl"} -m davinci'
#     return execute_bash_command(inference_cmd)


if __name__ == '__main__':
    prepare_dataset()
