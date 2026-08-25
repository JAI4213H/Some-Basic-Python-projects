from ollama import chat
##FUNCTION TO SUMMARISE THE MEMORY AFTER n AMOUNT OF CHAT
def summarise_memory(x: list): 
    memory_content = "  ".join([i["content"] for i in x])
    messages_format = [{
        
        
        "role" : "user",
        
        "content": f"Summarise the memory of model (dont use special characters such as * or anything else): {memory_content}"
    }]

    summarised_memory = chat(
        model="qwen3:1.7b",
        messages = messages_format,
        think = True
    )
    return summarised_memory.message.content

#WHILE LOOP TO GET PROMPTS FROM USERS AND STORING IN MEMORY SO THAT IT CAN BE USED AS REFRENCE
counter = 0
memory = []
while True:
    if counter > 2:
        counter = 0
        print("\n\nTrying To Summarise Memory\n\n")
        temp = summarise_memory(memory)
        memory.clear()
        memory.append(
            {"role":"system",
            "content" : f"Memory of whole chat is: {temp} "}
        )
        
        print("Memory Updated")
        print("\n",memory[0]["content"])
    prompt = str(input("Enter Your Prompt: "))
    
    memory.append({
        "role":"user",
        "content": prompt
    })

    output = chat(
        model="qwen3:1.7b",
        messages = memory,
        think = True
    )
    print(output.message.content)
    memory.append({
        "role": "assistant",
        "content": output.message.content
    })
    counter +=1
    
    
    
    
    
    
