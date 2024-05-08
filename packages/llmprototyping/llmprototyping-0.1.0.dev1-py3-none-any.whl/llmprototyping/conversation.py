from .llm_interface import Message, Response, LLMChatCompletion
from .serializable import Serializable

class Conversation(Serializable):
    @property
    def message_count(self):
        return len(self._messages)
    @property
    def messages(self):
        return self._messages
    
    def __init__(self, messages):
        self._messages = messages

    def add_message(self, message: Message):
        self._messages.append(message)

    def to_dict(self):
        return {
            'messages': [m.to_dict() for m in self.messages],
        }

    @staticmethod
    def from_dict(data):
        assert len(data) == 1
        return Conversation(messages=data['messages'])
