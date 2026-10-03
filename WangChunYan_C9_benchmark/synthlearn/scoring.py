"""Deterministic exact-match scoring and the learning metrics.

Scoring is exact string match on the single-letter output symbol — no human
judge, no partial credit, fully reproducible.
"""

from __future__ import annotations


def accuracy(model, algebra, items) -> float:
    """Fraction of ``items`` the model answers correctly."""
    if not items:
        return 0.0
    correct = sum(1 for e in items if model.predict(algebra, e) == algebra.answer(e))
    return correct / len(items)


def learning_gain(phase_b_acc: float, phase_a_acc: float) -> float:
    """Phase B accuracy minus Phase A accuracy: how much was learned from examples."""
    return phase_b_acc - phase_a_acc


def feedback_gain(phase_c_acc: float, phase_b_acc: float) -> float:
    """Phase C accuracy minus Phase B accuracy: improvement from corrective feedback."""
    return phase_c_acc - phase_b_acc


def feedback_accuracy(model, algebra, items) -> float:
    """Single-pass accuracy where a wrong answer is followed by the correct one.

    After each incorrect prediction the model receives ``on_feedback(expr, ans)``
    (if it supports it), then continues.  This is the operationalisation of the
    KSTAR loop ``A -> R -> ΔR -> update K -> A'``.
    """
    correct = 0
    for expr in items:
        pred = model.predict(algebra, expr)
        ans = algebra.answer(expr)
        if pred == ans:
            correct += 1
        elif hasattr(model, "on_feedback"):
            model.on_feedback(expr, ans, algebra)
    return correct / len(items)
