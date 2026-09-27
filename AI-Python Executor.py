from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "NotGonnaSayIt"
)
prompt = str(input("Enter the prompt"))

response = client.responses.create(
  model="openai/gpt-oss-20b",
  input=rf"{prompt} and dont add text like heres the python code, like only give to code no other nstruction. MAKE SURE NOT TO INCLUDE ``` python OR #!/usr/bin/env python3 just the code in tripple quatations",
  max_output_tokens=4096,
  top_p=1,
  temperature=1,
  stream=False,
  reasoning={"effort": "low"}
)


a = response.output_text
a = a.strip()

if a.startswith("'''") and a.endswith("'''"):
    a = a[3:-3].strip()
  
elif a.startswith('"""') and a.endswith('"""'):
    a = a[3:-3].strip()
elif a.startswith('```') and a.endswith('```'):
    a = a[3:-3].strip()



namespace = {}
exec(a,namespace)
print("all the functions and calls are", namespace.keys())
