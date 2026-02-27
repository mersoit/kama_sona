"""
agent.py
========

Defines the Agent class, which integrates the physical representation
of the simulated entity with its cognitive Mind.  The agent holds
position information, perceives the environment, generates actions
through its mind, and applies those actions to move around the world.
"""

from __future__ import annotations

from typing import List, Tuple, Optional
import pygame

from environment import Environment
from mind import Mind
from embodiment import EnvironmentAdapter


class Agent:
    """Embodied agent with a mind in a 2D environment."""

    def __init__(self, env: Environment, mind: Mind, adapter: EnvironmentAdapter | None = None) -> None:
        self.env = env
        self.mind = mind
        self.adapter = adapter or EnvironmentAdapter()
        self.x: float = env.width / 2.0
        self.y: float = 0.0
        self.radius: int = 10
        self.color: Tuple[int, int, int] = (255, 0, 0)
        # internal state
        self._last_sentence: Optional[List[str]] = None

    def perceive(self) -> dict:
        """Gather perception data from the environment."""
        return self.adapter.perceive(self.env, self)

    def act(self, action_tokens: List[str]) -> None:
        """Execute an action produced by the mind.

        The action is represented as a list of Toki Pona tokens.
        Currently supports very simple movements (tawa, lon) and
        placeholder interactions (moku etc.).
        """
        self.adapter.apply_action(self.env, self, action_tokens)

    def update(self, dt: float) -> List[str]:
        """Update agent state and produce an utterance.

        Returns the Toki Pona sentence produced by the mind.
        """
        perception = self.perceive()
        toki_sentence, action_tokens = self.mind.decide(perception)
        self.act(action_tokens)
        self._last_sentence = toki_sentence
        return toki_sentence

    def render(self, surface: pygame.Surface) -> None:
        """Draw the agent on the surface."""
        pygame.draw.circle(surface, self.color, (int(self.x), int(surface.get_height() - self.y)), self.radius)
