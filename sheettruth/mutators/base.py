"""Contract every mutator follows, plus the registry that discovers them.

Adding a new error type = add one file in this folder that defines a subclass of Mutator.
The registry finds it by import; nothing else needs to change.
"""
from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import Optional

from sheettruth.windows.cellinfo import CellContext


@dataclass
class Mutation:
    broken_formula: str      # the formula after we break it
    expected_formula: str    # the original, i.e. the fix
    error_type: str          # mutator name
    reason_template: str     # plain-English reason with the real labels filled in
    touched_cells: list[str] # cells the mutation depends on (for provenance and audits)


class Mutator:
    """Base class. Subclasses set `name` and implement applies() and mutate()."""

    name: str = "base"
    version: str = "1"

    def applies(self, ctx: CellContext) -> bool:
        """Return True only when breaking this cell produces a real, learnable error."""
        raise NotImplementedError

    def mutate(self, ctx: CellContext, rng) -> Optional[Mutation]:
        """Return a Mutation or None if, on closer look, no safe mutation exists."""
        raise NotImplementedError


_REGISTRY: dict[str, Mutator] = {}


def registry() -> dict[str, Mutator]:
    """Import every module in sheettruth.mutators and collect Mutator subclasses."""
    if _REGISTRY:
        return _REGISTRY
    import sheettruth.mutators as pkg

    for mod in pkgutil.iter_modules(pkg.__path__):
        if mod.name in ("base", "__init__"):
            continue
        m = importlib.import_module(f"sheettruth.mutators.{mod.name}")
        for obj in vars(m).values():
            if isinstance(obj, type) and issubclass(obj, Mutator) and obj is not Mutator:
                inst = obj()
                _REGISTRY[inst.name] = inst
    return _REGISTRY
