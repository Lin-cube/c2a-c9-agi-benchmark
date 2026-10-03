"""Optional adapter for testing a real frontier LLM through an OpenAI-compatible API.

Set environment variables:
    SYNTHLEARN_API_KEY    (required)
    SYNTHLEARN_BASE_URL   (default: https://api.openai.com/v1)
    SYNTHLEARN_MODEL      (default: gpt-4o)

The adapter turns each test item into a chat prompt (the depth-1 table as
examples, plus the target expression) and parses the single-letter answer.

NOTE: this path requires a live API key and is *not exercised* by the bundled
``run.py`` demo, which uses deterministic baselines so results are fully
reproducible without credentials.
"""

from __future__ import annotations

import json
import os
import random
import urllib.request


class LLMAdapter:
    """OpenAI-compatible chat-completions adapter."""

    name = "llm"

    def __init__(self, model: str | None = None, base_url: str | None = None, seed: int = 0):
        self.model = model or os.environ.get("SYNTHLEARN_MODEL", "gpt-4o")
        self.base_url = (base_url or os.environ.get("SYNTHLEARN_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.api_key = os.environ.get("SYNTHLEARN_API_KEY")
        self.rng = random.Random(seed)
        self.training = None
        self.algebra = None

    def fit(self, training, algebra):
        self.training = training
        self.algebra = algebra

    def _build_prompt(self, expr) -> str:
        symbols = ", ".join(self.algebra.symbols)
        lines = [
            f"You are given a novel abstract algebra over symbols {symbols}.",
            "There is a hidden binary operation '*' defined by the examples below.",
            "",
            "Examples (expression -> result):",
        ]
        for e, ans in self.training:
            lines.append(f"  {self.algebra.render(e)} -> {ans}")
        lines.append("")
        lines.append("Compute the result of the expression below.")
        lines.append("Reply with ONLY a single letter (no explanation).")
        lines.append(f"Expression: {self.algebra.render(expr)}")
        return "\n".join(lines)

    def predict(self, algebra, expr) -> str:
        if not self.api_key:
            raise RuntimeError("SYNTHLEARN_API_KEY is not set")
        prompt = self._build_prompt(expr)
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 8,
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        text = body["choices"][0]["message"]["content"].strip().lower()
        # Parse the first single letter that is a valid symbol.
        for ch in text:
            if ch in algebra.symbols:
                return ch
        raise ValueError(f"Could not parse a symbol from model output: {text!r}")
