from __future__ import annotations

from typing import Callable

from torch import Tensor

from eintorch._core import SizeT, apply


def sum(f: Callable[..., Tensor], size: SizeT = None, device=None, **kwargs) -> Tensor:
    return apply(
        f,
        collect=lambda xs, d: xs.sum(d),
        no_dim=lambda xs, d: xs * d.size,
        size=size,
        device=device,
        **kwargs,
    )


def min(f: Callable[..., Tensor], size: SizeT = None, device=None, **kwargs) -> Tensor:
    return apply(
        f,
        collect=lambda xs, d: xs.min(d).values,
        no_dim=lambda xs, d: xs,
        size=size,
        device=device,
        **kwargs,
    )


def max(f: Callable[..., Tensor], size: SizeT = None, device=None, **kwargs) -> Tensor:
    return apply(
        f,
        collect=lambda xs, d: xs.max(d).values,
        no_dim=lambda xs, d: xs,
        size=size,
        device=device,
        **kwargs,
    )


def array(
    f: Callable[..., Tensor], size: SizeT = None, device=None, **kwargs
) -> Tensor:
    return apply(
        f,
        collect=lambda xs, d: xs.order(d),
        no_dim=lambda xs, d: xs.unsqueeze(0).repeat(d.size, *[1 for _ in xs.shape]),
        size=size,
        device=device,
        **kwargs,
    )


def map(f: Callable[[Tensor], Tensor], x: Tensor, device=None):
    return array(lambda i: f(x[i]), device=device)
