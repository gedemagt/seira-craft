import itertools
from abc import ABC, abstractmethod
from typing import Any, List, Callable, TypeVar, Generic, Hashable

T = TypeVar("T")


class OverlapException(Exception):
    def __init__(self, msg: str, overlaps: List[T]):
        super().__init__(msg)
        self.overlaps = overlaps


class Crafter(ABC, Generic[T]):
    @abstractmethod
    def get_start(self, instance: T) -> Any:
        pass

    @abstractmethod
    def get_end(self, instance: T) -> Any:
        pass

    @abstractmethod
    def copy(
        self, instance: T, new_start: Any = None, new_end: Any = None, **kwargs
    ) -> T:
        pass

    def translate(self, instance: T, delta: Any) -> T:
        return self.copy(
            instance, self.get_start(instance) + delta, self.get_end(instance) + delta
        )

    def check_for_overlaps(
        self, sequence: List[T], group_by: Callable[[T], Any] = None
    ):
        sorted_sequence = sorted(sequence, key=self.get_start)

        overlaps = []

        for k, v in itertools.groupby(
            sorted_sequence, key=group_by if group_by else lambda _: 1
        ):
            sub_sequence = list(v)
            for x, y in zip(sub_sequence[:-1], sub_sequence[1:]):
                if self.overlaps(x, y):
                    overlaps.append((self.copy(x), self.copy(y)))
        if overlaps:
            raise OverlapException(f"Sequence has {len(overlaps)} overlaps", overlaps)

    def overlaps(self, i1: T, i2: T) -> bool:
        overlap = min(self.get_end(i1), self.get_end(i2)) - max(
            self.get_start(i1), self.get_start(i2)
        )
        return overlap > 0

    def insert(
        self,
        new_instance: T,
        sequence: List[T],
        group_by: Callable[[T], Hashable] = None,
        **kwargs,
    ) -> List[T]:
        result = []
        if group_by:
            to_merge_into = []
            for x in sequence:
                if group_by(x) == group_by(new_instance):
                    to_merge_into.append(x)
                else:
                    result.append(x)
            merged = self._insert_into_sequence(new_instance, to_merge_into, **kwargs)
            result += merged
        else:
            result = self._insert_into_sequence(new_instance, sequence, **kwargs)
        result.sort(key=lambda _x: self.get_start(_x))
        return result

    def _insert_into_sequence(self, new_instance: T, sequence: List[T], **kwargs):
        c_start = self.get_start(new_instance)
        c_end = self.get_end(new_instance)

        result = [new_instance]

        for v in sequence:
            v_start = self.get_start(v)
            v_end = self.get_end(v)
            if v_end <= c_start or v_start >= c_end:
                """
                        |--c--|
                |--v--|
                or
                |--c--|
                        |--v--|
                """
                result.append(self.copy(v, **kwargs))
            elif v_start < c_start < v_end <= c_end:
                """
                   |--c--|
                |--v--|
                """
                result.append(self.copy(v, new_end=c_start, **kwargs))
            elif v_end > c_end > v_start >= c_start:
                """
                |--c--|
                   |--v--|
                """
                result.append(self.copy(v, new_start=c_end, **kwargs))
            elif v_start < c_start and v_end > c_end:
                """
                  |--c--|
                |----v----|
                """
                new_v_left = self.copy(v, new_end=c_start, **kwargs)
                new_v_right = self.copy(v, new_start=c_end, **kwargs)

                result.append(new_v_left)
                result.append(new_v_right)

        return result

    def repeat(self, sequence: List[T], times: int) -> List[T]:
        for x in range(times):
            prev = sequence[-1]
            prev_start = self.get_start(prev)
            prev_end = self.get_end(prev)
            delta = prev_end - prev_start
            sequence.append(
                self.copy(prev, new_start=prev_end, new_end=prev_end + delta)
            )
        return sequence

    def repeat_all(self, sequence: List[T], times: int) -> List[T]:
        delta = self.get_end(sequence[-1]) - self.get_start(sequence[0])

        sub_seq = sequence.copy()
        for x in range(times):
            for y in sub_seq:
                sequence.append(self.translate(y, delta * (x + 1)))
        return sequence
