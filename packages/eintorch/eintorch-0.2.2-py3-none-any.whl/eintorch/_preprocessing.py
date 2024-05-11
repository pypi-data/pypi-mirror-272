from __future__ import annotations

from contextlib import contextmanager
from typing import Generic, TypeVar, List, Optional

import torch
from torch import Tensor

U = TypeVar("U")
V = TypeVar("V")


class ContextualTreeCache(Generic[V]):
    def __init__(self) -> None:
        self.cache: dict[V] = dict()
        self.parents_idx: List[int] = [-1]
        self.last_idx = -1

    @contextmanager
    def node(self):
        self.last_idx += 1
        self.parents_idx.append(self.last_idx)
        try:
            yield self.last_idx
        finally:
            self.parents_idx.pop()
            if self.parents_idx == [-1]:
                self.last_idx = -1
                self.cache = {}

    @contextmanager
    def new_children_set(self):
        self.last_idx = self.parents_idx[-1]
        try:
            yield self.last_idx
        finally:
            self.last_idx = self.parents_idx[-1]

    def get(self) -> Optional[V]:
        return self.cache[self.last_idx] if self.last_idx in self.cache else None

    def set(self, v: V):
        self.cache[self.last_idx] = v


class ConstraintTrackingTensor(Tensor):
    _constraints: set[int]

    @staticmethod
    def add_constraint(tensor, size):
        if isinstance(tensor, ConstraintTrackingTensor):
            if hasattr(tensor, "_constraints"):
                tensor._constraints.add(size)
            else:
                tensor._constraints = {size}

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        args_l = list(args)
        if func.__name__ == "__getitem__":
            if isinstance(args_l[1], ConstraintTrackingTensor):
                ConstraintTrackingTensor.add_constraint(args_l[1], args_l[0].shape[0])
            elif isinstance(args_l[1], tuple) and any(
                isinstance(i, ConstraintTrackingTensor) for i in args_l[1]
            ):
                for i, (size, index) in enumerate(zip(args_l[0].shape, args_l[1])):
                    ConstraintTrackingTensor.add_constraint(index, size)

            if isinstance(args_l[0], ConstraintTrackingTensor):
                args_l[0] = torch.tensor(args_l[0])
            return torch.tensor(
                super().__torch_function__(func, types, tuple(args_l), kwargs)
            )
        if kwargs is None:
            kwargs = {}
        return super().__torch_function__(func, types, tuple(args_l), kwargs)
