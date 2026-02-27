"""
environment.py
================

Defines the 2D world used by the Kama Sona simulation.  The
Environment class is responsible for storing world objects,
applying simple physics (gravity and sunlight) and rendering
them using Pygame.  This module should remain agnostic of
agent logic; it merely updates and draws objects.
"""

from __future__ import annotations

import math
import pygame
from typing import List, Tuple


class WorldObject:
    """Representation of an object in the world.

    This simple class stores position, velocity and whether the
    object is affected by gravity.  It can be extended to include
    sprites, collision shapes and interactions.
    """

    def __init__(self, x: float, y: float, movable: bool = False) -> None:
        self.x = x
        self.y = y
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.movable = movable
        self.radius = 10  # radius for drawing

    def update(self, dt: float, gravity: float) -> None:
        """Apply physics updates to the object."""
        if self.movable:
            self.velocity_y -= gravity * dt
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt

            # Simple ground collision: stop at y = 0
            if self.y < 0:
                self.y = 0
                self.velocity_y = 0

    def render(self, surface: pygame.Surface) -> None:
        """Draw the object as a circle."""
        pygame.draw.circle(surface, (0, 0, 255), (int(self.x), int(surface.get_height() - self.y)), self.radius)

    def get_state(self) -> dict:
        """Return a serialisable representation of the object state."""
        return {
            "position": (self.x, self.y),
            "movable": self.movable,
        }


class Environment:
    """A 2D world with basic physics and lighting."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.objects: List[WorldObject] = []
        self.gravity = 9.8
        self.sunlight = 1.0  # 0–1 intensity
        self.time = 0.0

        # Populate the world with a few objects
        # Example: a static tree and a movable rock
        self.objects.append(WorldObject(x=200, y=0, movable=False))
        self.objects.append(WorldObject(x=400, y=100, movable=True))

    def update_physics(self, dt: float) -> None:
        """Update world state over a time step."""
        self.time += dt
        # Sunlight oscillates with time
        self.sunlight = max(0.0, (math.sin(self.time / 10.0) + 1.0) / 2.0)
        for obj in self.objects:
            obj.update(dt, gravity=self.gravity)

    def render(self, surface: pygame.Surface) -> None:
        """Render the world and its objects."""
        # Draw a simple ground
        pygame.draw.rect(surface, (50, 200, 50), (0, surface.get_height() - 10, surface.get_width(), 10))
        # Draw objects
        for obj in self.objects:
            obj.render(surface)
