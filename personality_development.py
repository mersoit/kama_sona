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

        action_trait_bias = {
            "moku": {"openness": 0.2},
            "lon": {"conscientiousness": 0.1},
            "tawa": {"extraversion": 0.2},
        }
        trait_bias = action_trait_bias.get(action_verb, {})

        novelty_weight = 0.6
        conscientious_positive = 0.3
        conscientious_negative = 0.2
        extraversion_positive = 0.4
        extraversion_negative = 0.2
        extraversion_mood = 0.2
        agreeableness_positive = 0.25
        agreeableness_negative = 0.1
        neuroticism_negative = 0.5
        neuroticism_positive = 0.15

        deltas = {
            "openness": (novelty - 0.5) * novelty_weight + trait_bias.get("openness", 0.0),
            "conscientiousness": (
                conscientious_positive * positive
                - conscientious_negative * negative
                + trait_bias.get("conscientiousness", 0.0)
            ),
            "extraversion": (
                extraversion_positive * positive
                - extraversion_negative * negative
                + extraversion_mood * mood
                + trait_bias.get("extraversion", 0.0)
            ),
            "agreeableness": agreeableness_positive * positive - agreeableness_negative * negative,
            "neuroticism": neuroticism_negative * negative - neuroticism_positive * positive,
        }

        for trait, delta in deltas.items():
            current = getattr(personality, trait)
            baseline_value = getattr(baseline, trait)
            adjusted = current + (self.pace * delta) - (self.pace * self.baseline_pull * (current - baseline_value))
            setattr(personality, trait, _clamp(adjusted))

        return personality
