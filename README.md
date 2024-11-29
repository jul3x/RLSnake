# RLSnake

## Intro

Simple snake game playable by human and other types of implemented bots (including RLAgent).

## Purpose

I wanted to dive a lil bit into Reinforcement Learning world to check possibilities of unsupervised learning agents on my own.
...nd I have never ever created a Snake game so, why not?

## Agents

* **Human** - just allows to control the game using keyboard arrows
* **Random** - random bot performing random actions, just a boilerplate for some more complex agents
* **Aware** - bot that is aware of the food placement and tries to reach it
* **CollisionAware** - similar to aware but this agent is also aware of the danger and tries to not collide with the obstacles
* **RLTrain** - agent trained using Reinforcement Learning technique using Neural Network with 11 inputs, 1024 neurons in hidden layer and output of length 3.

## RLTrain agent

Agent uses NN with 11, 1024 and 3 neurons in each layer. Input state is described as a vector with 11 boolean values:

* Danger is one step ahead,
* Danger is on the right,
* Danger is on the left,
* Agent is moving to the west,
* Agent is moving to the east,
* Agent is moving to the north,
* Agent is moving to the south,
* Food is on the west,
* Food is on the east,
* Food is on the north,
* Food is on the south.

This is pretty standard input vector for the Snake RL agent.
I experimented with other types of vectors such as (I must point that I have no theoretical background on the topic whatsoever):

* Additional dimension for current length of the snake - I didn't see any improvement in agent's behaviour.
* Whole board state embedded into vector of HEIGHT_X * HEIGHT_Y size with values: 
  * 0 - blank,
  * 1 - snake cell, 
  * 2, 3, 4, 5 - snake head rotated to east, west, north, south direction,
  * 6 - food,
  * 7 - food covered by snake cell. 
  
  This approach failed - possibly because of too short training time.

Agent produces output vector of size 3 consisting of float numbers. The largest one number wins and determines action for the agent.
The biggest 1st, 2nd and 3rd number represents consecutively heading straight, turning right and turning left.

Reward - nothing: 0, eating food: 10, getting killed: -10.

Simple as that.

## Usage

- Install python (I tested it with Python 3.11) with pygame
- Install pytorch and numpy to use RLAgent
- Run using `python -m snake.main --type {AGENT_TYPE} --n-games 1000 --fps 500` - `AGENT_TYPE: HUMAN, RANDOM, AWARE, COLLISION_AWARE, RL_TRAIN`

