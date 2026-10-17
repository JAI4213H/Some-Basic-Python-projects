
from openai import OpenAI
import inspect


class ModelSet:
    def __init__(self, api_key, model="openai/gpt-oss-20b"):
        self.api_key = api_key
        self.model = model
        self.namespace = {}

    def connect(self, prompt):
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )

        try:
            response = client.responses.create(
                model=self.model,
                input=(
                    f"{prompt}\n\n"
                    "Return only Python code. Do not include explanations "
                    "or Markdown code fences."
                ),
                max_output_tokens=4096,
                top_p=1,
                temperature=1,
                reasoning={"effort": "low"}
            )
            return response.output_text.strip()

        except Exception as e:
            print("API error:", e)
            print("Check your API key:",
                  "https://build.nvidia.com/settings/api-keys")
            return None

    def process(self, code):
        if not code:
            print("No code received.")
            return

        code = code.strip()

        if code.startswith("```") and code.endswith("```"):
            lines = code.splitlines()
            code = "\n".join(lines[1:-1]).strip()
        elif (
            (code.startswith("'''") and code.endswith("'''"))
            or (code.startswith('"""') and code.endswith('"""'))
        ):
            code = code[3:-3].strip()

        namespace = {}

        try:
            exec(code, namespace)

            self.namespace = {
                name: obj
                for name, obj in namespace.items()
                if name != "__builtins__"
            }

            print("Functions and variables:",
                  list(self.namespace.keys()))

        except Exception as e:
            print("Code execution failed:", e)

    def show_functions(self):
        print("Available functions:")

        for name, obj in self.namespace.items():
            if inspect.isfunction(obj):
                print(name)
