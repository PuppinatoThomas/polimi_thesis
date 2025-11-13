from __future__ import annotations

from abc import ABC, abstractmethod


class BasePrompt(ABC):

    def __init__(self, user_message: str, system_message: str = None):
        self.user_message = user_message
        self.system_message = system_message

    @abstractmethod
    def copy(self) -> BasePrompt:
        pass

class QuestionPrompt(BasePrompt):

    def __init__(self, prompt_id: int, user_message: str, system_message: str = None):
        super().__init__(user_message, system_message)
        self.id = prompt_id

    def copy(self) -> QuestionPrompt:
        return QuestionPrompt(self.id, self.user_message, self.system_message)

class EvaluationPrompt(BasePrompt):

    def __init__(self, batch: str, user_message: str, system_message: str = None):
        super().__init__(user_message, system_message)
        self.batch = batch

    def copy(self) -> EvaluationPrompt:
        return EvaluationPrompt(self.batch, self.user_message, self.system_message)