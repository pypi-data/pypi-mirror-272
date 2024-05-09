from logging import getLogger
from typing import List

import yaml

logger = getLogger(__name__)


class Settings:
    def __init__(self, **kwargs):
        self.model = kwargs.get('model')
        self.temperature = kwargs.get('temperature')
        self.max_tokens = kwargs.get('max_tokens')
        self.top_p = kwargs.get('top_p')
        self.logit_bias = kwargs.get('logit_bias', {})
        self.stop = kwargs.get('stop', None)
        self.user = kwargs.get('user')
        self.n = kwargs.get('n')
        self.stream = kwargs.get('stream')
        self.presence_penalty = kwargs.get('presence_penalty')
        self.frequency_penalty = kwargs.get('frequency_penalty')


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }


class Variable:
    def __init__(self, name, required):
        self.name = name
        self.required = required


class PromptTemplate:
    def __init__(self, version, name, provider, settings, messages, variables):
        self.version = version
        self.name = name
        self.provider = provider
        self.settings = settings
        self.messages = messages
        self.variables = variables


class Prompt:
    def __init__(self, provider: str, settings: Settings, messages: List[Message]):
        self.provider = provider
        self.settings = settings
        self.messages = messages


def camel_to_snake(name):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')


def load_yaml_to_template(prompt_file_path):
    with open(prompt_file_path, 'r') as file:
        data = yaml.safe_load(file)

    settings = Settings(**{camel_to_snake(k): v for k, v in data['settings'].items()})
    messages = [Message(**m) for m in data['messages']]
    variables = [Variable(**v) for v in data['variables']]
    return PromptTemplate(data['version'], data['name'], data['provider'], settings, messages, variables)


def inject_variables(template, variables):
    if variables is None:
        variables = {}
    declared_vars = {var.name: var for var in template.variables}
    content_vars = {}

    # Scan for variables in messages and prepare content replacements
    for msg in template.messages:
        for part in msg.content.split("{"):
            if "}" in part:
                var_name = part.split("}")[0]
                if var_name in declared_vars:
                    content_vars[var_name] = True
                    if var_name not in variables:
                        if declared_vars[var_name].required:
                            raise ValueError(f"Required variable '{var_name}' is missing.")
                        else:
                            variables[var_name] = ''
                elif var_name not in variables:
                    raise ValueError(f"Undeclared variable '{var_name}' is used in messages.")

    # Check for extra variables not used in content
    for var in variables:
        if var not in content_vars:
            raise ValueError(f"Variable '{var}' provided but not declared in any message.")

    # Replace variables in messages
    new_messages = []
    for msg in template.messages:
        content = msg.content.format(**variables)
        new_messages.append(Message(msg.role, content))

    return Prompt(template.provider, template.settings, new_messages)


def load_prompt(prompt_file_path, variables=None) -> Prompt:
    template = load_yaml_to_template(prompt_file_path)
    return inject_variables(template, variables)
