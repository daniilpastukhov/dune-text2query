# prepare dataset
#echo Preparing dataset...
#python prepare_dataset.py

# validate dataset
echo Validating dataset...
openai tools fine_tunes.prepare_data -f data/finetune_dataset.jsonl

# fine-tune model
echo Fine-tuning model...
openai api fine_tunes.create \
  -t data/finetune_dataset_prepared.jsonl \
  -m curie \
  --suffix "dune_sql" \
  --n_epochs 5 \
  --batch_size 128
