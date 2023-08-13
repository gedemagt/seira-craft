from collections import defaultdict
from typing import Generic, TypeVar, List, Callable, Hashable, Dict

from seira_craft.crafter import Crafter

T = TypeVar("T")


class Siera(Generic[T]):
    def __init__(
        self,
        crafter: Crafter[T],
        group_by: Callable[[T], Hashable] = None,
        sequence: List[T] = None,
    ):
        self.crafter = crafter
        self._sequences: Dict[Hashable, List[T]] = defaultdict(list)
        if sequence:
            for instance in sequence:
                self._sequences[group_by(instance)].append(instance)
        self._group_by = group_by if group_by else lambda _: 1

    def insert(self, new_instance: T, **kwargs) -> "Siera":
        key = self._group_by(new_instance)
        self._sequences[key] = self.crafter.insert(
            new_instance, self._sequences[key], **kwargs
        )
        return self

    def repeat(self, times: int) -> "Siera":
        for key, val in self._sequences.items():
            self._sequences[key] = self.crafter.repeat(val, times)
        return self

    def repeat_all(self, times: int) -> "Siera":
        for key, val in self._sequences.items():
            self._sequences[key] = self.crafter.repeat_all(val, times)
        return self

    def sequence(self) -> List[T]:
        result = []
        for x in self._sequences.values():
            result.extend(x)
        return sorted(result, key=self.crafter.get_start)
