"""Allocate case-insensitive unique identifiers with numeric suffixes."""

from __future__ import annotations

from collections.abc import Iterable


def allocate_unique_id(base_id: str, existing_ids: set[str]) -> str:
    """Return ``base_id`` or ``base_id-2``, ``base_id-3``, … until free.

    Comparison against ``existing_ids`` is case-insensitive (``casefold``).
    """
    if base_id.casefold() not in existing_ids:
        return base_id
    suffix = 2
    while True:
        candidate = f"{base_id}-{suffix}"
        if candidate.casefold() not in existing_ids:
            return candidate
        suffix += 1


def id_taken(
    candidate: str,
    existing_ids: Iterable[str],
    *,
    excluding: str | None = None,
) -> bool:
    """Return True if ``candidate`` collides with another id (strip + casefold).

    ``excluding`` skips one exact existing id (the object being renamed/edited).
    """
    folded = candidate.strip().casefold()
    for existing in existing_ids:
        if excluding is not None and existing == excluding:
            continue
        if existing.strip().casefold() == folded:
            return True
    return False


def expand_ids_for_quantity(
    base_id: str,
    quantity: int,
    reserved: set[str],
) -> list[str] | None:
    """Expand ``base_id`` into ``quantity`` unique ids, mutating ``reserved``.

    - If ``base_id`` (casefold) is already in ``reserved``, return ``None``.
    - If ``quantity <= 1``, reserve and return ``[base_id]``.
    - If ``quantity > 1``, reserve ``base_id`` as a family prefix and return
      ``base-1``, ``base-2``, … skipping any suffix already reserved.

    ``reserved`` must hold casefolded ids. Newly claimed ids are added to it.
    """
    folded = base_id.casefold()
    if folded in reserved:
        return None

    reserved.add(folded)
    if quantity <= 1:
        return [base_id]

    generated: list[str] = []
    suffix = 1
    while len(generated) < quantity:
        candidate = f"{base_id}-{suffix}"
        suffix += 1
        candidate_key = candidate.casefold()
        if candidate_key in reserved:
            continue
        reserved.add(candidate_key)
        generated.append(candidate)
    return generated
