"""Procedural generation of expression datasets."""

from __future__ import annotations

import random

from .algebra import Algebra


def random_tree(rng: random.Random, n_symbols: int, leaves: int):
    """Return a random full binary tree with exactly ``leaves`` leaves.

    ``leaves`` is the complexity knob: 2 = a single operation (depth 1),
    3+ = nested compositions (depth >= 2).  The tree shape is chosen randomly,
    so both left- and right-nested forms appear (important because random
    Cayley tables are non-associative).
    """
    if leaves == 1:
        return rng.randrange(n_symbols)
    left = rng.randint(1, leaves - 1)
    return (
        random_tree(rng, n_symbols, left),
        random_tree(rng, n_symbols, leaves - left),
    )


def all_depth1_pairs(n_symbols: int):
    """All ordered ``(i, j)`` single-operation expressions — the full table.

    These are the training examples: learning them completely determines the
    binary operation, so the answers to all deeper compositions are uniquely
    defined (the task is well-posed, never underdetermined).
    """
    return [(i, j) for i in range(n_symbols) for j in range(n_symbols)]


def generate_phase_items(
    algebra: Algebra,
    n_items: int,
    min_leaves: int,
    max_leaves: int,
    seed: int = 0,
):
    """Generate ``n_items`` unique expressions with leaves in the given range."""
    rng = random.Random(seed)
    items = []
    seen = set()
    while len(items) < n_items:
        leaves = rng.randint(min_leaves, max_leaves)
        expr = random_tree(rng, algebra.n, leaves)
        key = repr(expr)
        if key in seen:
            continue
        seen.add(key)
        items.append(expr)
    return items
