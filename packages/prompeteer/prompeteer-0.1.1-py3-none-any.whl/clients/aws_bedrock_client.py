import json

import boto3

from clients.llm_client import LLMClient


class AwsBedrockClient(LLMClient):
    def __init__(self):
        self.bedrock_runtime_client = boto3.client(
            service_name="bedrock-runtime", region_name="us-east-1"
        )

    def call(self, model, messages, parameters) -> str:
        request = {
            "anthropic_version": model,
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": messages}],
                }
            ],
        }

        response = self.bedrock_runtime_client.invoke_model(
            modelId=model,
            body=json.dumps(request)
        )

        return json.loads(response.get('body').read())
