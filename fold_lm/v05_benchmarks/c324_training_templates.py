"""C324 authoring component: select TRAIN templates without changing labels.

This is not a scientific runner or an experiment registration. The caller must
first validate the accepted dataset, prompt hashes and source protection. Pass
TRAIN-only projections of C319 length prompts and C321 interior prompts; the
component does not load artifacts, construct a model, tokenize or fit weights.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

OLD_PROFILES = ("repeat", "shared_prefix", "shared_suffix")
INTERIOR_PROFILES = ("u_dominant", "balanced", "v_dominant")
LENGTHS = (2, 3, 4)
ARMS = ("original", "interior4")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class TrainingViews:
    """Immutable input strings and separate teacher targets, in source-row order."""
    tables: Mapping[tuple[int, str], tuple[str, ...]]
    source_ids: tuple[str | int, ...]
    targets: tuple[int, ...]


def _sequence(value: Any, label: str) -> Sequence:
    require(isinstance(value, (list, tuple)), label + ": expected list/tuple")
    return value


def _rows(rows: Any) -> tuple[tuple[str | int, ...], tuple[int, ...]]:
    rows = _sequence(rows, "TRAIN rows")
    require(bool(rows), "empty TRAIN rows")
    ids, targets = [], []
    for row in rows:
        require(isinstance(row, Mapping), "TRAIN row is not a mapping")
        require({"id", "language", "entities", "values", "permutation", "query", "target"} <= row.keys(),
                "incomplete TRAIN row")
        require(type(row["id"]) in (str, int), "invalid source ID")
        require(row["language"] in ("en", "ja"), "invalid language")
        entities = tuple(_sequence(row["entities"], "entities"))
        values = tuple(_sequence(row["values"], "values"))
        order = tuple(_sequence(row["permutation"], "permutation"))
        require(len(entities) == 2 and len(values) == 2, "two facts required")
        require(all(type(v) is int and 0 <= v < 3 for v in entities)
                and len(set(entities)) == 2, "invalid entity pair")
        require(all(type(v) is int and 0 <= v < 4 for v in values)
                and len(set(values)) == 2, "invalid value pair")
        require(all(type(v) is int for v in order)
                and order in (entities, entities[::-1]), "invalid fact permutation")
        require(type(row["query"]) is int and row["query"] in entities, "invalid query")
        require(type(row["target"]) is int
                and row["target"] == 48 + values[entities.index(row["query"])], "target binding")
        ids.append(row["id"])
        targets.append(row["target"])
    require(len(set(ids)) == len(ids), "duplicate source IDs")
    return tuple(ids), tuple(targets)


def _normals(records: Any, ids: tuple, targets: tuple, label: str) -> tuple[str, ...]:
    records = _sequence(records, label)
    require(len(records) == len(ids), label + ": row count")
    result = []
    for record, source_id, target in zip(records, ids, targets, strict=True):
        require(isinstance(record, Mapping)
                and {"source_id", "target", "views"} <= record.keys(), label + ": record schema")
        require(type(record["source_id"]) is type(source_id)
                and record["source_id"] == source_id, label + ": source alignment")
        require(type(record["target"]) is int and record["target"] == target, label + ": target alignment")
        views = record["views"]
        require(isinstance(views, Mapping) and "normal" in views, label + ": normal view missing")
        text = views["normal"]
        require(type(text) is str and bool(text) and "\x00" not in text, label + ": invalid normal text")
        try:
            text.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError(label + ": invalid UTF-8 text") from exc
        result.append(text)
    return tuple(result)


def build_training_views(
    train_rows: Sequence[Mapping[str, Any]],
    original_train: Mapping[str, Mapping[str, Sequence[Mapping[str, Any]]]],
    interior_train: Mapping[str, Sequence[Mapping[str, Any]]] | None,
    *,
    arm: str,
) -> TrainingViews:
    """Replace only length-four TRAIN strings, preserving profile slot and row order.

    original_train is {str(length): original_prompts[str(length)]['TRAIN']}
    for lengths 2, 3, 4. interior_train is C321.new_prompts(data)['TRAIN'].
    Extra/missing original lengths and profile slots are rejected. The original
    arm never reads interior_train. Masked views never enter the returned tables.
    This validates alignment, not canonical artifact hashes or renderer semantics.
    """
    require(type(arm) is str and arm in ARMS, "unregistered training arm")
    ids, targets = _rows(train_rows)
    require(isinstance(original_train, Mapping)
            and set(original_train) == {str(n) for n in LENGTHS}, "original length inventory")
    tables = {}
    for length in LENGTHS:
        profiles = original_train[str(length)]
        require(isinstance(profiles, Mapping)
                and set(profiles) == set(OLD_PROFILES), "original profile inventory")
        for profile in OLD_PROFILES:
            tables[length, profile] = _normals(profiles[profile], ids, targets, f"old/{length}/{profile}")
    if arm == "interior4":
        require(isinstance(interior_train, Mapping)
                and set(interior_train) == set(INTERIOR_PROFILES), "interior profile inventory")
        for old, new in zip(OLD_PROFILES, INTERIOR_PROFILES, strict=True):
            tables[4, old] = _normals(interior_train[new], ids, targets, "interior/" + new)
    return TrainingViews(MappingProxyType(tables), ids, targets)
