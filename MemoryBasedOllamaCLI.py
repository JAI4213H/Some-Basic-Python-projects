from ollama import chat
##FUNCTION TO SUMMARISE THE MEMORY AFTER n AMOUNT OF CHAT

the_real_content= """
Summarise the following conversation memory carefully and create a compact but information-rich summary that can be used by the model in future conversations.

Your main goal is to preserve all information that may be useful for understanding future user requests or continuing the conversation.

Make sure to preserve:
1. Important facts and information discussed in the conversation.
2. User preferences, requirements, goals, and constraints.
3. Important decisions that were made.
4. Important technical details, code-related information, configurations, or approaches.
5. Names of important projects, models, tools, libraries, datasets, or technologies.
6. Important problems, errors, solutions, and fixes that were discovered.
7. Any ongoing tasks, unfinished work, or plans that may need to be continued later.
8. Important credentials, keys, tokens, usernames, passwords, API keys, or other sensitive authentication information if they were explicitly provided and are necessary for future use.
9. Any other information that would prevent the model from losing important context from the previous conversation.

Do not include unnecessary small talk, repeated information, or information that has no value for future conversations.

Do not invent, assume, or change any information. Only summarize information that is actually present in the memory.

Keep the summary concise enough to fit into the model context, but detailed enough that the model can understand the important history without needing the original conversation.

Do not use special formatting, markdown, bullet symbols, asterisks, or unnecessary special characters. Write the summary as clear plain text.

Here is the memory that needs to be summarized:


"""





def summarise_memory(x: list):
    memory_content = "  ".join([i["content"] for i in x])
    messages_format = [{
        
        
        "role" : "user",
        
        "content": f"{the_real_content},{memory_content}"
    }]

    summarised_memory = chat(
        model="qwen3:1.7b",
        messages = messages_format,
        think = False
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
        memory.append({
            "role": "system",
            "content": f"Memory of whole chat is: {temp}"
        })

        print("Memory Updated")
        print("\n", memory[0]["content"])

    prompt = str(input("Enter Your Prompt: "))

    memory.append({
        "role": "user",
        "content": prompt
    })

    output = chat(
        model="qwen3:1.7b",
        messages=memory,
        think=True,
        stream=True
    )
    full_response = ""

    for i in output:
        token = i.message.content
        print(token, end="", flush=True)
        full_response += token
    print()
    
    memory.append({
        "role": "assistant",
        "content": full_response
    })

    counter += 1
    
    
    
    
    
    
