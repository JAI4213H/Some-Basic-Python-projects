

import torch
import transformers
import bitsandbytes

from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig

model_name= "Qwen/Qwen2.5-Coder-3B-Instruct"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(model_name,quantization_config=quant_config,device_map="auto")

format = [ # just fore ideaaa
    {"role": "system", "content": "You are a helpful assistant but you try to add some humour in the code you generate"},
    {"role": "user", "content":"Generate me a function code in python to find the factorial of number"}
]

text = tokenizer.apply_chat_template(
    format,
    tokenize=False,
    retirn_tensor="pt"
)

input = tokenizer(text,return_tensors="pt").to(model.device)







pip install -U transformers peft datasets accelerate bitsandbytes

from peft import LoraConfig,get_peft_model, prepare_model_for_kbit_training

model = prepare_model_for_kbit_training(model)

l_config = LoraConfig(
    r = 8,
    lora_alpha = 16,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj"
    ],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model,l_config)

model.print_trainable_parameters()

import pandas as pd

df = pd.read_json("dataset.json")

df.head()

def format_example(row):
  message = [
      {"role":"system","content":"You are the master of Python language"},

      {"role":"user","content":row["instruction"]},

      {"role":"assistant", "content": row["response"]}
  ]
  return tokenizer.apply_chat_template(
      message,
      tokenize=False,
      add_generation_prompt=False
  )

df["text"] = df.apply(format_example,axis=1)



from datasets import Dataset

dataset = Dataset.from_pandas(df)

def token(example):
    tokens = tokenizer(
        example["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

    tokens["labels"] = tokens["input_ids"].copy()

    return tokens

tokenized_dataset = dataset.map(token,batched=True)

split_dataset = tokenized_dataset.train_test_split(test_size=0.2,shuffle=True,seed=42)

train_dataset = split_dataset["train"]
eval_dataset = split_dataset["test"]

from transformers import TrainingArguments, Trainer

training_arge = TrainingArguments(
    output_dir="./qwen-python-lora",

    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    max_grad_norm=0.3,
    num_train_epochs=3,

    lr_scheduler_type="constant",
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=100,
    report_to="none"

)

trainer = Trainer(
    model = model,
    train_dataset = train_dataset,
    eval_dataset = eval_dataset,
    args = training_arge

    )

trainer.train()

print(next(model.parameters()).device)

from google.colab import drive

drive.mount("/content/drive")

save_path = "/content/drive/MyDrive/qwen-python-lora"

import os

os.makedirs(save_path, exist_ok=True)

model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

