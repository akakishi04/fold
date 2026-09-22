"""Opt-in checked fixed-W capsule preparation; CPU float64 inference only.

No answer or bias is cached. Normal tensor mutation is tracked by identity/version.
External unsafe alias writes, .data mutation, autograd and concurrency are outside this contract.
The existing ResponseCapsule and memory-bank reference paths remain unchanged.
"""
from __future__ import annotations
from dataclasses import dataclass
import torch


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _tensor(x):
    _require(isinstance(x, torch.Tensor), "tensor required")
    _require(x.dtype == torch.float64 and x.device.type == "cpu", "CPU float64 required")
    _require(not x.requires_grad, "inference-only preparation")


def _capsule_tensors(capsule):
    return (capsule.y0, capsule.g, capsule.V, capsule.K)


def _stamps(tensors):
    return tuple((id(x), x._version) for x in tensors)


@dataclass(frozen=True, eq=False)
class PreparedCapsule:
    capsule: object
    W: torch.Tensor
    LU: torch.Tensor
    pivots: torch.Tensor
    stamps: tuple


def prepare(capsule, W, *, context=()):
    """Validate the same SPD condition as the reference, then factor I+W@K once."""
    tensors = _capsule_tensors(capsule)
    for x in tensors + (W,):
        _tensor(x)
        _require(bool(torch.isfinite(x).all()), "NUMERIC_UNSAFE: nonfinite preparation")
    y0,g,V,K = tensors
    r = K.shape[-1] if K.ndim == 2 else 0
    _require(r > 0 and K.shape == (r,r) and W.shape == (r,r)
             and g.shape == (r,) and y0.ndim == 1 and V.shape == (y0.numel(),r),
             "OUT_OF_SCOPE: unbatched fixed-port shapes required")
    _require(torch.equal(W,W.mT), "NUMERIC_UNSAFE: exact symmetric W required")
    for x in context:
        _tensor(x)
    eye = torch.eye(r,dtype=W.dtype,device=W.device)
    L = torch.linalg.cholesky(K)
    _,info = torch.linalg.cholesky_ex(eye+L.mT@W@L)
    _require(not bool(torch.any(info != 0)), "NUMERIC_UNSAFE: updated system not SPD")
    LU,pivots = torch.linalg.lu_factor(eye+W@K)
    retained = W.detach().clone()
    _require(bool(torch.isfinite(LU).all()), "NUMERIC_UNSAFE: factor nonfinite")
    stamps = _stamps(tensors+tuple(context)+(retained,LU,pivots))
    return PreparedCapsule(capsule,retained,LU,pivots,stamps)


def response(cache, capsule, W, bias, *, context=()):
    """Recompute the current-bias response; reject changed preparation rather than fallback."""
    _require(isinstance(cache,PreparedCapsule) and cache.capsule is capsule,
             "STALE_PREPARATION: capsule identity")
    _require(_stamps(_capsule_tensors(capsule)+tuple(context)+(cache.W,cache.LU,cache.pivots))
             == cache.stamps, "STALE_PREPARATION: mutated/replaced capsule, context or cache")
    _tensor(W); _tensor(bias)
    _require(W.shape == cache.W.shape and bias.shape == (cache.W.shape[0],),
             "OUT_OF_SCOPE: update shape")
    _require(torch.equal(W,cache.W), "STALE_PREPARATION: aggregate W changed")
    _require(bool(torch.isfinite(bias).all()), "NUMERIC_UNSAFE: nonfinite current bias")
    rhs = (bias-W@capsule.g).unsqueeze(-1)
    correction = torch.linalg.lu_solve(cache.LU,cache.pivots,rhs)
    result = capsule.y0+(capsule.V@correction).squeeze(-1)
    _require(bool(torch.isfinite(result).all()), "NUMERIC_UNSAFE: nonfinite response")
    return result


def extra_tensor_bytes(cache):
    storages = {x.untyped_storage().data_ptr():x.untyped_storage().nbytes()
                for x in (cache.W,cache.LU,cache.pivots)}
    return sum(storages.values())
