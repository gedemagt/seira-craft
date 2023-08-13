from copy import deepcopy
from typing import Any, Dict, Generic

from seira_craft.crafter import Crafter, T


class DefaultCrafter(Crafter[T], Generic[T]):
    def __init__(self, start_att: str = "start", end_att: str = "end"):
        self.start_att = start_att
        self.end_att = end_att

    def get_start(self, instance: T) -> Any:
        return getattr(instance, self.start_att)

    def get_end(self, instance: T) -> Any:
        return getattr(instance, self.end_att)

    def copy(
        self, instance: T, new_start: Any = None, new_end: Any = None, **kwargs
    ) -> T:
        new = instance.copy()
        if new_start:
            setattr(new, self.start_att, new_start)
        if new_end:
            setattr(new, self.end_att, new_end)

        for key, value in kwargs.items():
            setattr(new, key, value)
        return new


class DictCrafter(Crafter[Dict]):
    def __init__(
        self, start_att: str = "start", end_att: str = "end", deep_copy: bool = False
    ):
        self.start_att = start_att
        self.end_att = end_att
        self.deep_copy = deep_copy

    def get_start(self, instance: Dict) -> Any:
        return instance[self.start_att]

    def get_end(self, instance: Dict) -> Any:
        return instance[self.end_att]

    def copy(
        self, instance: Dict, new_start: Any = None, new_end: Any = None, **kwargs
    ) -> T:
        if self.deep_copy:
            new_instance = deepcopy(instance)
        else:
            new_instance = instance.copy()

        if new_start:
            new_instance[self.start_att] = new_start
        if new_end:
            new_instance[self.end_att] = new_end

        new_instance.update(kwargs)

        return new_instance
