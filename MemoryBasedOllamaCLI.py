import threading
from ollama import chat




counter = 0
memory = []

summarising = False

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






##GIVE SNAPSHOT OF THE MEMORY SO THAT IT WONT INTERFARE IN NEW MEMORY CREATED USING CHAT IN PARALLEL
##PROVIDE SNAPSHOT TO IT SO THAT IT WONT TAKE VALUE FROM CURRENT MEMORY AND WHICH MIGHT AFFECT SUMMARISING
def summarise_memory(memory_snapshot):
    memory_content = "  ".join(
        i["content"] for i in memory_snapshot
    )

    messages_format = [{
        "role": "user",
        "content": f"{the_real_content}\n\n{memory_content}"
    }]

    summarised_memory = chat(
        model="qwen3:1.7b",
        messages=messages_format,
        think=False
    )

    return summarised_memory.message.content


def show_memory():
    """Used to show/display the stored memory"""
    global memory
    return memory[0]["content"]

def background_summarise(memory_snapshot):
    global memory
    global summarising

    print("\n\n[Background] Summarising memory...\n")

    try:
        summary = summarise_memory(memory_snapshot)

        # Update memory after summarisation finishes
        memory.clear()

        memory.append({
            "role": "system",
            "content": f"Memory of whole chat is: {summary}"
        })

        print("\n[Background] Memory Updated!\n")

    except Exception as e:
        print("\n[Background] Error:", e)

    finally:
        summarising = False

while True:

    # Start background summarisation
    if counter > 2 and not summarising:

        counter = 0
        summarising = True

        # Give the thread a copy, not the actual memory
        memory_snapshot = memory.copy()

        thread = threading.Thread(
            target=background_summarise,
            args=(memory_snapshot,)
        )

        thread.start()


    # mai n program continues immediately
    prompt = input("\nEnter Your Prompt: ")

    memory.append({
        "role": "user",
        "content": prompt
    })


    output = chat(
        model="qwen3:1.7b",
        messages=memory,
        think=True,
        stream=True,
        tools=[show_memory,]
    )


    full_response = ""
    tool_calls = []

    for i in output:

        if i.message.content:
            token = i.message.content
            print(token, end="", flush=True)
            full_response += token

        if i.message.tool_calls:
            tool_calls.extend(i.message.tool_calls)

    print()


    # Handle tool calls
    if tool_calls:

        memory.append({
            "role": "assistant",
            "tool_calls": tool_calls
        })


        for tool_call in tool_calls:

            if tool_call.function.name == "show_memory":

                result = show_memory()

                memory.append({
                    "role": "tool",
                    "content": result
                })


        # Send tool result back to the model
        output = chat(
            model="qwen3:1.7b",
            messages=memory,
            think=True,
            stream=True,
            tools=[show_memory,]
        )


        full_response = ""

        for i in output:

            if i.message.content:
                token = i.message.content
                print(token, end="", flush=True)
                full_response += token

        print()


    memory.append({
        "role": "assistant",
        "content": full_response
    })


    counter += 1
