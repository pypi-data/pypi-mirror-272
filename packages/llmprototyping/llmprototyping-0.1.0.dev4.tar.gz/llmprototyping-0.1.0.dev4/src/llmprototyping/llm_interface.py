from abc import ABC, abstractmethod
from typing import List
from .serializable import Serializable
from .factory import Factory
   
class Message(Serializable):
    @property
    def role(self):
        return self._role
    @property
    def content(self):
        return self._content

    def __init__(self, content, role='user'):
        self._role = role
        self._content = content

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }

    @staticmethod
    def from_dict(data):
        assert len(data) == 2
        return Message(role=data['role'], content=data['content'])

    def show(self):
        print(f"Message role:{self.role} content:")
        print(self.content)


class Response:
    @property
    def message(self):
        return self._message
    @property
    def input_token_count(self):
        return self._input_token_count
    @property
    def output_token_count(self):
        return self._output_token_count
    @property
    def is_success(self):
        return self._is_success
    @property
    def status_code(self):
        return self._status_code
    @property
    def error(self):
        return self._error

    def show_header(self):
        if not self.is_success:
            print(f"Response failure; status:{self.status_code} error:{self.error}")
        else:
            print(f"Response successful; tokens: i:{self.input_token_count} o:{self.output_token_count}")

    def show(self):
        self.show_header()
        if self.is_success:
            self.message.show()

    @staticmethod
    def error_response(status_code, error):
        return Response(status_code = status_code, error = error, is_success=False)

    def __init__(self,
                 message = None,
                 is_success:bool=True,
                 status_code=200,
                 error=None,
                 input_token_count=None,
                 output_token_count=None):
        self._message = message
        self._input_token_count = input_token_count
        self._output_token_count = output_token_count
        self._status_code = status_code
        self._error = error
        self._is_success = is_success
        if is_success:
            assert isinstance(message, Message)
            assert isinstance(input_token_count, int)
            assert isinstance(output_token_count, int)


class LLMChatCompletion(ABC):
    @property
    @abstractmethod
    def context_size(self):
        raise NotImplemented()

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        # this returns an LLM object
        raise NotImplemented()

    @abstractmethod
    def query(self, messages:List[Message], json_response=False, temperature=1.0):
        # this returns a Response
        raise NotImplemented()

class LLMChatCompletionFactory(Factory):
    _class = LLMChatCompletion

