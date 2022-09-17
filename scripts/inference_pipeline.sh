# prepare dataset
echo Preparing dataset...
python prepare_dataset.py

# validate dataset
echo Validating dataset...
openai tools fine_tunes.prepare_data -f data/finetune_dataset.jsonl

# fine-tune model
echo Fine-tuning model...
openai tools fine_tunes.fine_tune \
  -f data/finetune_dataset.jsonl \
  -m davinci \
  --suffix "dune_sql" \
  --n_epochs 4 \  # larger -> work better
  --batch_size 128