from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Sequence, Union, Optional

import torch
from functorch.dim import Dim
from functorch.dim import Tensor as DTensor
from functorch.dim import dims
from torch import Tensor

from eintorch._preprocessing import ConstraintTrackingTensor, ContextualTreeCache
from eintorch._utils import (
    count_positional_args,
    is_autoreload_enabled,
    get_first_arg_name,
)

TensorLike = Union[Tensor, DTensor]
SizeT = Union[None, int, Sequence[Union[None, int]]]


@dataclass
class DimTraceData:
    size: int
    device: Optional[Union[str, torch.device]]


tensor_cache: ContextualTreeCache[DimTraceData] = ContextualTreeCache()


def _apply_single_dim(
    f: Callable[[int], TensorLike],
    collect: Callable[[DTensor, Dim], TensorLike],
    no_dim: Callable[[TensorLike, Dim], TensorLike],
    dim_name: str,
    size: int | None = None,
    device=None,
) -> TensorLike:
    # TODO: allow the dim to be passed as a kwarg for size
    # no_dim is called if the dim we're 'iterating' over isn't in the returned expression
    with tensor_cache.node():
        cached_dims = tensor_cache.get()
        if cached_dims is None:
            with tensor_cache.new_children_set():
                idx = ConstraintTrackingTensor(torch.tensor(0))
                reified = f(idx)  # type: ignore

            if size is None:
                constraints = getattr(idx, "_constraints", [])
                if len(constraints) > 1:
                    # TODO: name the dimension argument with the error
                    constraint_assignments = ", ".join(
                        f"{dim_name}={i}" for i in constraints
                    )
                    raise ValueError(
                        f"Error: incompatible size constraints for dimension {dim_name} (found {constraint_assignments}). Manually specify the size of this dimension using `{dim_name}=...`."
                    )
                elif len(constraints) == 0:
                    raise ValueError(
                        f"Error: Unable to infer size of dimension {dim_name}. Manually specify the size of this dimension using `{dim_name}=...`."
                    )
                else:
                    size = list(constraints)[0]
            cached_dims = DimTraceData(size=size, device=reified.device)
            tensor_cache.set(cached_dims)

        size = cached_dims.size
        reified_device = cached_dims.device

        with tensor_cache.new_children_set():
            dim = dims(sizes=[size])
            if size is not None:
                idx = torch.arange(size).to(
                    reified_device if device is None else device
                )
                xs = f(idx[dim])  # type: ignore
            else:
                xs = f(dim)

        if isinstance(xs, DTensor) and hash(dim) in [hash(i) for i in xs.dims]:
            result = collect(xs, dim)
        else:
            result = no_dim(xs, dim)

        return result


def apply(
    f: Callable[..., Tensor],
    collect: Callable[[Tensor, Dim], Tensor],
    no_dim: Callable[[Tensor, Dim], Tensor],
    size: SizeT = None,
    device=None,
    **kwargs,
) -> Tensor:
    if is_autoreload_enabled():
        raise RuntimeError(
            "Autoreload is enabled, which prevents `eintorch` from working properly. Please disable autoreload."
        )

    n_args = count_positional_args(f)
    assert n_args is not None, "f may only have positional arguments"
    if size is None:
        size_arr = [None for _ in range(n_args)]
    elif not isinstance(size, Sequence):
        size_arr = [size]
    else:
        size_arr = size
    assert len(size_arr) == n_args

    fun: Any = (
        (
            lambda dim: apply(
                partial(f, dim), collect, no_dim, size_arr[1:], device, **kwargs
            )
        )
        if len(size_arr) > 1
        else f
    )

    size = size_arr[0]
    dim_name = get_first_arg_name(f)
    dim_size = kwargs[dim_name] if dim_name in kwargs else None
    assert not ((size is not None) and (dim_size is not None))
    if dim_size is not None:
        size = dim_size

    return _apply_single_dim(
        fun,
        collect,
        no_dim,
        dim_name,
        size,
        device,
    )
