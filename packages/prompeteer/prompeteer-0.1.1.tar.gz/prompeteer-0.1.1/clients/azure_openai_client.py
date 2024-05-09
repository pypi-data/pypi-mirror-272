import openai

from clients.llm_client import LLMClient


class AzureOpenAiClient(LLMClient):
    def __init__(self, azure_openai_api_key: str, azure_openai_api_base: str):
        self.azure_openai_api_key = azure_openai_api_key
        self.azure_openai_base = azure_openai_api_base
        openai.api_key = azure_openai_api_key
        openai.api_base = azure_openai_api_base
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'

    def call(self, engine, messages, parameters) -> str:
        try:
            if '3.5' in engine:
                model = engine.replace('3.5', '35')
            else:
                model = engine

            response = openai.ChatCompletion.create(
                engine=model,
                messages=messages,
                **parameters
            )
            return response.choices[0].message["content"]
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
