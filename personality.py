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

    def influence_action(self, actions: list[list[str]], mood: float = 0.0) -> list[str]:
        """Select an action candidate based on personality and current mood.

        Args:
            actions: A list of possible action token sequences.
            mood: Current mood (valence) from the agent's emotion state.

        Returns:
            One of the action sequences from ``actions``.

        The selection algorithm biases choices using the Big Five
        traits and the agent's mood.  High extraversion encourages
        movement (``tawa``) and social engagement; high openness
        promotes exploratory actions.  High conscientiousness and
        agreeableness favour the default "lon" (no movement) when
        mood is negative, while high neuroticism discourages risky
        behaviour.  If no recognised biases apply, the first action
        is returned as a default.
        """
        if not actions:
            return []

        # Map actions to symbolic roles for biasing
        # Index 0: "tawa" (move), index 1: "lon" (idle), index 2: other (e.g. "moku")
        move_index = 0
        idle_index = 1 if len(actions) > 1 else 0
        other_index = 2 if len(actions) > 2 else 0

        # Determine preferences based on traits and mood
        # Start with equal probabilities
        weights = [1.0 for _ in actions]

        # Extraversion and positive mood favour movement
        weights[move_index] += 2.0 * (self.extraversion + max(mood, 0.0))
        # Openness encourages exploration, map to first non‑idle action
        if len(actions) > other_index:
            weights[other_index] += 1.5 * self.openness
        # Conscientiousness and agreeableness encourage staying put when mood is low
        if mood < 0:
            weights[idle_index] += 2.0 * (self.conscientiousness + self.agreeableness)
        # Neuroticism discourages risky or uncertain actions (other_index)
        if len(actions) > other_index:
            weights[other_index] -= self.neuroticism
        # Ensure weights are non‑negative
        weights = [max(w, 0.0) for w in weights]
        # Normalise weights
        total = sum(weights)
        if total > 0:
            weights = [w / total for w in weights]
        else:
            weights = [1.0 / len(weights) for _ in weights]

        # Choose action by sampling according to weights
        import random
        r = random.random()
        cumulative = 0.0
        for idx, weight in enumerate(weights):
            cumulative += weight
            if r <= cumulative:
                return actions[idx]
        return actions[0]
