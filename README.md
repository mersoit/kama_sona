# Kama Sona

This repository contains a **proof‑of‑concept simulation game** that
implements a layered artificial agent inspired by the design
outlined in the accompanying research report.  The agent inhabits a
simple 2D world and communicates in **Toki Pona**, a minimalist
constructed language.  Its cognitive architecture is divided into a
**subconscious**, **ego**, **superego**, and includes a
**universal-grammar component** and a **Big Five personality**.

## Features

- **2D Environment**: A world with basic physics (gravity and
  sunlight) implemented using Pygame.  Objects fall under gravity and
  sunlight intensity oscillates over time.
- **Embodied Agent**: A red circle representing the character in the
  world.  The agent perceives its surroundings, decides on actions,
  moves around, and speaks in Toki Pona.
- **Layered Mind**: The `mind` module contains a Subconscious that
  records experiences, an Ego that mediates actions and enforces
  grammar, and a Superego that learns simple normative rules via
  reinforcement.
- **Grammar Module**: The `grammar.py` module implements a
  simplified Toki Pona grammar based on subject–verb–object order
  with particles `li` and `e`【282361990344596†L18-L124】.  It validates and
  canonicalises sentences to prevent ungrammatical output.
- **Personality**: The `personality.py` module stores the Big Five
  personality traits【321794716508073†L346-L355】 and biases action
  selection.
- **Personality Development**: The `personality_development.py` module
  evolves traits at a slow, human-like pace while anchoring the agent's
  baseline temperament so uniqueness persists across environments.
- **Emotion Module**: The `emotion.py` module tracks the agent's mood,
  updating it based on rewards and clamping values between -1 and 1, and
  influences action selection.

## Modular Integration

The simulation is designed to let the mind travel to new environments.
To plug the same agent into other worlds (including modded games), swap
the `EnvironmentAdapter` in `embodiment.py`. The adapter translates
world-specific perception data and applies actions, while the mind and
personality development modules remain unchanged.

## Getting Started

1. Install Pygame:

   ```bash
   pip install pygame
   ```

2. Run the simulation:

   ```bash
   python main.py
   ```

You should see a window with a red agent on a green ground.  The
agent will move rightwards (`tawa`) when sunlight is high and say
`mi tawa` in Toki Pona.  The utterance appears at the bottom of the
window.  Feel free to experiment by expanding the grammar, adding
new verbs/objects, and implementing richer personality influence.

## Repository Structure

```
main.py        # Entry point for running the game
environment.py # World and physics logic
agent.py       # Embodied agent that integrates the mind with the environment
mind.py        # Subconscious, Ego and Superego implementation
grammar.py     # Simplified Toki Pona grammar and lexicon
personality.py # Big Five personality data structure
personality_development.py # Gradual personality evolution module
embodiment.py  # Environment adapter for plugging into new worlds
README.md      # Overview and instructions
```

## Future Work

This project is a starting point for a richer simulation.  Future
enhancements could include:

- A fuller lexicon and grammar for Toki Pona, including prepositions,
  questions and context particles【282361990344596†L18-L124】.
- A transformer‑based Ego layer that uses the grammar as a filter.
- Sophisticated personality‑based decision making reflecting the
  Big Five traits【321794716508073†L346-L355】.
- A chat interface allowing the user to talk to the agent in Toki Pona and influence its behaviour.
- Cross-platform portability: port the game to web and mobile platforms (e.g., using Kivy or Pyodide) so the agent can run in diverse environments.
- Richer emotion modelling: extend the emotion system to represent a range of moods and affective states, enabling more nuanced and human-like responses.
