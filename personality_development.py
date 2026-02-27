"""
personality_development.py
==========================

Provides a slow, experience-driven personality development module. The
goal is to let traits evolve at a human-like pace while still retaining
each agent's unique baseline temperament.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from personality import Personality


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


@dataclass
class PersonalityDevelopment:
    """Gradually adjust personality traits based on lived experience.

    The action-to-trait bias map nudges traits based on the agent's
    expressed verbs (e.g., "tawa" encourages extraversion).
    """

    pace: float = 0.02
    baseline_pull: float = 0.15
    baseline: Optional[Personality] = None
    novelty_threshold: float = 5.0
    novelty_center: float = 0.5
    novelty_weight: float = 0.6
    conscientious_positive: float = 0.3
    conscientious_negative: float = 0.2
    extraversion_positive: float = 0.4
    extraversion_negative: float = 0.2
    extraversion_mood: float = 0.2
    agreeableness_positive: float = 0.25
    agreeableness_negative: float = 0.1
    neuroticism_negative: float = 0.5
    neuroticism_positive: float = 0.15
    action_trait_bias: dict[str, dict[str, float]] = field(
        default_factory=lambda: {
            "moku": {"openness": 0.2},
            "lon": {"conscientiousness": 0.1},
            "tawa": {"extraversion": 0.2},
        }
    )

    def _ensure_baseline(self, personality: Personality) -> None:
        if self.baseline is None:
            self.baseline = Personality(
                openness=personality.openness,
                conscientiousness=personality.conscientiousness,
                extraversion=personality.extraversion,
                agreeableness=personality.agreeableness,
                neuroticism=personality.neuroticism,
            )

    def _calculate_novelty(self, perception: dict) -> float:
        if self.novelty_threshold <= 0:
            return 0.0
        return min(1.0, len(perception.get("objects", [])) / self.novelty_threshold)

    def update(
        self,
        personality: Personality,
        perception: dict,
        action_tokens: List[str],
        reward: float,
        mood: float,
    ) -> Personality:
        """Evolve the supplied personality in place and return it."""
        self._ensure_baseline(personality)
        baseline = self.baseline
        if baseline is None:
            return personality

        novelty = self._calculate_novelty(perception)
        positive = max(reward, 0.0)
        negative = max(-reward, 0.0)
        action_verb = action_tokens[0] if action_tokens else None
        trait_bias = self.action_trait_bias.get(action_verb, {}) if action_verb else {}

        deltas = {
            "openness": (novelty - self.novelty_center) * self.novelty_weight + trait_bias.get("openness", 0.0),
            "conscientiousness": (
                self.conscientious_positive * positive
                - self.conscientious_negative * negative
                + trait_bias.get("conscientiousness", 0.0)
            ),
            "extraversion": (
                self.extraversion_positive * positive
                - self.extraversion_negative * negative
                + self.extraversion_mood * mood
                + trait_bias.get("extraversion", 0.0)
            ),
            "agreeableness": self.agreeableness_positive * positive - self.agreeableness_negative * negative,
            "neuroticism": self.neuroticism_negative * negative - self.neuroticism_positive * positive,
        }

        for trait, delta in deltas.items():
            current = getattr(personality, trait)
            baseline_value = getattr(baseline, trait)
            adjusted = current + (self.pace * delta) - (self.pace * self.baseline_pull * (current - baseline_value))
            setattr(personality, trait, _clamp(adjusted))

        return personality
