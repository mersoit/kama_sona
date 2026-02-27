"""
embodiment.py
=============

Defines a lightweight adapter between the agent and its environment.
Swap this module to plug the same mind into different worlds, such as
modded games or alternate simulators.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Environment
    from agent import Agent


@dataclass
class EnvironmentAdapter:
    """Default adapter for the built-in 2D environment."""

    step_size: float = 5.0

    def perceive(self, env: "Environment", agent: "Agent") -> dict:
        objects_state = [obj.get_state() for obj in env.objects]
        return {
            "position": (agent.x, agent.y),
            "objects": objects_state,
            "sunlight": env.sunlight,
        }

    def apply_action(self, env: "Environment", agent: "Agent", action_tokens: List[str]) -> None:
        if not action_tokens:
            return
        verb = action_tokens[0]
        if verb == "tawa":
            agent.x = max(agent.radius, min(env.width - agent.radius, agent.x + self.step_size))
        elif verb == "lon":
            pass
