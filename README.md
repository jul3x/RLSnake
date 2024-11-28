# RL-Snake

# Intro

Simple snake game playable by human and other types of implemented bots.

## Purpose

I wanted to dive a lil bit into Reinforcement Learning world to check possibilities of learning agents on my own.
And I have never ever created a Snake game so - additional plus for that.

## Agents

* **Human** - just allows to control the game using keyboard arrows
- **Random** - random bot performing random actions, just a boilerplate for some more complex agents
- **Aware** - bot that is aware of the food placement and tries to reach it
- **CollisionAware** - similar to aware but this agent is also aware of the danger and tries to not collide with the obstacles

## Usage

- Install python (I tested it with Python 3.11) with pygame
- Run using `python -m snake.main --type {AGENT_TYPE}` - HUMAN, RANDOM, AWARE, COLLISION_AWARE
