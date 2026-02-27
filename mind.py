"""
mind.py
=======

Defines the cognitive layers of the Kama Sona agent: Subconscious,
Ego and Superego.  The Mind class orchestrates these layers to
process perceptions, choose actions and produce Toki Pona
utterances.
"""

from __future__ import annotations

import random
from typing import List, Tuple, Any

from grammar import TokiPonaGrammar
from personality import Personality
from personality_development import PersonalityDevelopment
from emotion import Emotion


class Subconscious:
    """Low‑level memory and associative processing."""

    def __init__(self) -> None:
        # Keep a simple memory of past perceptions and actions
        self.memory: List[Tuple[dict, List[str], List[str], float]] = []

    def process(self, perception: dict) -> Any:
        """Process perception and return a latent state.

        In a real implementation, this would update neural state or
        integrate sensor data.  For now we just return the perception.
        """
        return perception

    def record(self, perception: dict, sentence: List[str], action: List[str], reward: float) -> None:
        """Record an experience for potential future learning."""
        self.memory.append((perception, sentence, action, reward))


class Superego:
    """High‑level normative reasoning based on reinforcement."""

    def __init__(self) -> None:
        self.rules: dict[str, float] = {}

    def get_norms(self) -> dict[str, float]:
        return self.rules

    def update(self, action: List[str], reward: float) -> None:
        """Update normative strength of an action.

        This simplistic implementation treats the action sequence
        concatenated as a key; positive rewards strengthen it; negative
        rewards weaken it.
        """
        key = " ".join(action)
        self.rules[key] = self.rules.get(key, 0.0) + reward
        # Remove rules with negative weight
        if self.rules[key] <= 0:
            del self.rules[key]


class EgoModel:
    """Mediator between perception and action, enforcing grammar and personality."""

    def __init__(self, grammar: TokiPonaGrammar, personality: Personality) -> None:
        self.grammar = grammar
        self.personality = personality
        # Predefined possible actions for demonstration
        self.action_candidates = [
            ["tawa"],
            ["lon"],
            ["moku"],
        ]
    def generate(self, latent_state: Any, norms: dict[str, float], mood: float) -> Tuple[List[str], List[str]]:
        """Generate a sentence and an associated action. placeholder implementation selects an action based on
        personality, constructs a simple sentence describing the
        action, and returns both.
        """
        # Choose an action candidate using personality bias
        action = self.personality.influence_action(self.action_candidates, mood)
        # Generate a simple declarative sentence: subject verb [object]
        subject = "mi"
        verb = action[0] if action else "lon"
        tokens = [subject, verb]
        # Validate and canonicalise using grammar
        tokens = self.grammar.canonicalise(tokens)
        return tokens, action


class Mind:
    """Composite mind that coordinates subconscious, superego and ego."""

    def __init__(
        self,
        grammar: TokiPonaGrammar,
        personality: Personality,
        development: PersonalityDevelopment | None = None,
    ) -> None:
        self.subconscious = Subconscious()
        self.emotion = Emotion()
        self.superego = Superego()
        self.personality = personality
        self.ego = EgoModel(grammar=grammar, personality=personality)
        self.development = development or PersonalityDevelopment()

    def decide(self, perception: dict) -> Tuple[List[str], List[str]]:
        """Given a perception, produce a Toki Pona sentence and an action."""

        latent_state = self.subconscious.process(perception)
        norms = self.superego.get_norms()
        sentence, action = self.ego.generate(latent_state, norms, self.emotion.mood)
        # Evaluate outcome (placeholder reward)
        reward = self.evaluate_outcome(perception, action)
        self.emotion.update(reward)
        self.development.update(self.personality, perception, action, reward, self.emotion.mood)
        # Update superego and record memory
        self.superego.update(action, reward)
        self.subconscious.record(perception, sentence, action, reward)
        return sentence, action

    def evaluate_outcome(self, perception: dict, action: List[str]) -> float:
        """Compute a reward for the action given the perception.

        This simplistic reward function encourages movement when
        sunlight is high and penalises standing still in darkness.
        """
        sunlight = perception.get("sunlight", 0.0)
        if not action:
            return -0.1
        if action[0] == "tawa":
            return sunlight
        else:
            return 0.0
