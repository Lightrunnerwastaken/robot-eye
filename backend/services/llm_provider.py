from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMResponse:
    prompt: str
    completion: str


class LLMProvider:
    """Mockable abstraction for language model completions."""

    def complete(self, prompt: str) -> LLMResponse:
        # This mock simply echoes the prompt. Replace with a real LLM call.
        completion = (
            "\n".join([
                "Synthesized by NeuroLearn's mock LLM:",
                prompt,
                "-- Ende der Demo-Antwort --",
            ])
        )
        return LLMResponse(prompt=prompt, completion=completion)


provider = LLMProvider()
