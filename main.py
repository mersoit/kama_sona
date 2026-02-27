"""
Entry point for the Kama Sona simulation game.

This script initialises the environment, agent and mind and runs the
main game loop.  The game uses Pygame for rendering and event handling,
but this file only contains the high‑level loop; details of the
environment and agent behaviour are defined in separate modules.

See environment.py for the 2D world implementation and agent.py for
the agent and mind integration.
"""

import pygame
from environment import Environment
from agent import Agent
from mind import Mind
from grammar import TokiPonaGrammar
from personality import Personality


def main() -> None:
    """Run the simulation until the user closes the window."""
    # Initialise Pygame and create a window
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Kama Sona Simulation")

    # Create environment and agent
    env = Environment(width=width, height=height)
    grammar = TokiPonaGrammar()
    personality = Personality(openness=0.5, conscientiousness=0.5,
                              extraversion=0.5, agreeableness=0.5,
                              neuroticism=0.5)
    mind = Mind(grammar=grammar, personality=personality)
    agent = Agent(env=env, mind=mind)

    # Clock for frame rate control
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # delta time in seconds

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Additional input handling (e.g., chat) can be added here.

        # Update physics and agent
        env.update_physics(dt)
        toki_sentence = agent.update(dt)

        # Clear screen and draw environment
        screen.fill((255, 255, 255))  # white background
        env.render(screen)
        agent.render(screen)

        # Render the agent's utterance as text at bottom of screen
        if toki_sentence:
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(" ".join(toki_sentence), True, (0, 0, 0))
            screen.blit(text_surface, (10, height - 30))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
