import torch
from transformers import set_seed
from transformers import AutoTokenizer
from transformers import pipeline
from transformers import AutoModelForCausalLM
set_seed(10)
x = str(input("Enter the Line you want to complete: "))
prompt = x
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-0.5B")

x = 1
while True:
    if x == 0:
        break
    tokenized_ids = tokenizer(prompt,return_tensors="pt").input_ids
    output = model(tokenized_ids).logits[0,-1]
    mp_tensor = output.argmax()
    
    top_10 = torch.topk(output.softmax(dim=0),10)
    
    for i,j in zip(top_10.values,top_10.indices):
        print(f"{tokenizer.decode(j.item()):<10} {i.item():.3%}")
    print("------------------------------------")
    x = int(input("Enter 0 or 1"))
    
    prompt += tokenizer.decode(output.argmax().item())
    print(f"New prompt is {prompt}")
