"""
personality.py
==============

Defines a Personality class representing an agent's Big Five personality
traits.  Each trait is a floating‑point value in the range 0–1.  The
personality influences the Ego's decision‑making; for example,
high "openness" encourages exploratory actions.
"""

from dataclasses import dataclass


@dataclass
class Personality:
    """Container for the Big Five personality traits."""

    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

    def influence_action(self, actions: list[list[str]]) -> list[str]:
        """Choose an action from a list based on personality biases.

        This is a placeholder implementation that simply returns the
        first action.  A more sophisticated implementation could rank
        actions based on each trait: high extraversion might favour
        socially oriented actions, while high neuroticism might
        discourage risky behaviour.
        """
        return actions[0] if actions else []
