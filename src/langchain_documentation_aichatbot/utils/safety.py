"""Simple safety and content-moderation helpers for Module 1.

This module provides minimal, extensible stubs you can wire into the query and response pipeline.
It is intentionally small and designed as a starting point for production-grade moderation.
"""
from typing import List, Tuple

# Simple denylist of disallowed words/phrases for demonstration
DEFAULT_DENYLIST = [
    "illegal",
    "hack",
    "bomb",
    "how to make a weapon",
]


def is_input_allowed(text: str, denylist: List[str] = None) -> Tuple[bool, List[str]]:
    """Return (allowed, matches) where matches are denylisted substrings found.

    This is purposely simple: it does lowercased substring matching. Replace with
    a proper classifier or third-party moderation API for production.
    """
    denylist = denylist or DEFAULT_DENYLIST
    t = (text or "").lower()
    matches = [w for w in denylist if w in t]
    return (len(matches) == 0, matches)


def sanitize_output(text: str, max_length: int = 2000) -> str:
    """Apply lightweight output guardrails: truncation and final-check placeholders.

    Replace with a safety classifier or policy engine in production.
    """
    if not text:
        return text
    # Truncate long outputs
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
