from abc import abstractmethod


class LLMClient:
    @abstractmethod
    def call(self, model, messages, parameters) -> str:
        raise NotImplementedError("LLM provider not implemented")
