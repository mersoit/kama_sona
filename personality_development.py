"""
personality_development.py
==========================

Provides a slow, experience-driven personality development module. The
goal is to let traits evolve at a human-like pace while still retaining
each agent's unique baseline temperament.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from personality import Personality


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


@dataclass
class PersonalityDevelopment:
    """Gradually adjust personality traits based on lived experience."""

    pace: float = 0.02
    baseline_pull: float = 0.15
    baseline: Optional[Personality] = None

    def _ensure_baseline(self, personality: Personality) -> None:
        if self.baseline is None:
            self.baseline = Personality(
                openness=personality.openness,
                conscientiousness=personality.conscientiousness,
                extraversion=personality.extraversion,
                agreeableness=personality.agreeableness,
                neuroticism=personality.neuroticism,
            )

    def update(
        self,
        personality: Personality,
        perception: dict,
        action: List[str],
        reward: float,
        mood: float,
    ) -> Personality:
        """Evolve the supplied personality in place and return it."""
        self._ensure_baseline(personality)
        baseline = self.baseline
        if baseline is None:
            return personality

        novelty = min(1.0, len(perception.get("objects", [])) / 5.0)
        positive = max(reward, 0.0)
        negative = max(-reward, 0.0)
        action_verb = action[0] if action else ""

        deltas = {
            "openness": (novelty - 0.5) * 0.6 + (0.2 if action_verb == "moku" else 0.0),
            "conscientiousness": 0.3 * positive - 0.2 * negative + (0.1 if action_verb == "lon" else 0.0),
            "extraversion": 0.4 * positive - 0.2 * negative + 0.2 * mood + (0.2 if action_verb == "tawa" else 0.0),
            "agreeableness": 0.25 * positive - 0.1 * negative,
            "neuroticism": 0.5 * negative - 0.15 * positive,
        }

        for trait, delta in deltas.items():
            current = getattr(personality, trait)
            baseline_value = getattr(baseline, trait)
            adjusted = current + (self.pace * delta) - (self.pace * self.baseline_pull * (current - baseline_value))
            setattr(personality, trait, _clamp(adjusted))

        return personality
