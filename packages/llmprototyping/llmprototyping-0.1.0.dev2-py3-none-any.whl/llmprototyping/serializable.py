import json
from abc import ABC, abstractmethod

class Serializable(ABC):
    @abstractmethod
    def to_dict(self):
        raise NotImplemented()
    @staticmethod
    @abstractmethod
    def from_dict(data):
        raise NotImplemented()

    def to_json(self):
        return json.dumps(self.to_dict())
    @classmethod
    def from_json(cls,json_string):
        data = json.loads(json_string)
        return cls.from_dict(data)