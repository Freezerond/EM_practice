from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str):
        self.__path = path
        self.__parts_path = self.__path.split('.')

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.passage(data=instance.payload)

    def __set__(self, instance, value):
        data, last = self.passage(data=instance.payload, for_set=True)
        if data is not None:
            data[last] = value

    def passage(self, data: dict, for_set: bool = False):
        *parents, last = self.__parts_path
        for part in parents:
            if not isinstance(data, dict) or part not in data:
                return None if not for_set else (None, None)
            data = data[part]

        if for_set:
            return data, last

        return data.get(last) if isinstance(data, dict) else None