from typing import Any

class Emotion:
    """A simple emotion model tracking the agent's mood."""

    def __init__(self, mood: float = 0.0) -> None:
        """Initialize the mood of the agent.

        Args:
            mood: Initial mood between -1.0 (very negative) and 1.0 (very positive).
        """
        # Clamp initial mood to the allowed range
        self.mood = max(-1.0, min(1.0, mood))

    def update(self, reward: float) -> None:
        """Update mood based on a reward signal.

        Args:
            reward: The reinforcement signal from the environment. Positive rewards increase mood,
                    negative rewards decrease mood.
        """
        # Adjust mood according to reward
        self.mood += reward
        # Clamp mood between -1 and 1
        if self.mood > 1.0:
            self.mood = 1.0
        elif self.mood < -1.0:
            self.mood = -1.0
