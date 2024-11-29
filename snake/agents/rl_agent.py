import torch
import random
import numpy as np
from collections import deque
from snake.game import Direction
from .rl.model import Linear_QNet, QTrainer
from .agent import Agent

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.002  #learning rate


class RLAgent(Agent):

    def __init__(self, snake, board):
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 1024, 3)
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)
        self.score = 0
        self.move = None
        self.state_old = None
        super().__init__(snake, board)

    def get_state(self) -> np.array:
        point_l = (self.snake.pos[0][0] - 1, self.snake.pos[0][1])
        point_r = (self.snake.pos[0][0] + 1, self.snake.pos[0][1])
        point_u = (self.snake.pos[0][0], self.snake.pos[0][1] - 1)
        point_d = (self.snake.pos[0][0], self.snake.pos[0][1] + 1)
        dir_l = self.snake.dir == Direction.LEFT
        dir_r = self.snake.dir == Direction.RIGHT
        dir_u = self.snake.dir == Direction.UP
        dir_d = self.snake.dir == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and self.snake.collision(self.board, point_r))
            or (dir_l and self.snake.collision(self.board, point_l))
            or (dir_u and self.snake.collision(self.board, point_u))
            or (dir_d and self.snake.collision(self.board, point_d)),

            # Danger right
            (dir_u and self.snake.collision(self.board, point_r))
            or (dir_d and self.snake.collision(self.board, point_l))
            or (dir_l and self.snake.collision(self.board, point_u))
            or (dir_r and self.snake.collision(self.board, point_d)),

            # Danger left
            (dir_d and self.snake.collision(self.board, point_r))
            or (dir_u and self.snake.collision(self.board, point_l))
            or (dir_r and self.snake.collision(self.board, point_u))
            or (dir_l and self.snake.collision(self.board, point_d)),

            # Movement direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food position relative to snake
            self.board.food[0] < self.snake.pos[0][0],
            self.board.food[0] > self.snake.pos[0][0],
            self.board.food[1] < self.snake.pos[0][1],
            self.board.food[1] > self.snake.pos[0][1],
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action_embedding(self, state):
        self.epsilon = 100 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 2000) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def get_action(self):
        self.state_old = self.get_state()
        self.move = self.get_action_embedding(self.state_old)
        if np.array_equal(self.move, [1, 0, 0]):
            return self.snake.dir
        if np.array_equal(self.move, [0, 1, 0]):
            if self.snake.dir == Direction.UP:
                return Direction.RIGHT
            if self.snake.dir == Direction.RIGHT:
                return Direction.DOWN
            if self.snake.dir == Direction.DOWN:
                return Direction.LEFT
            if self.snake.dir == Direction.LEFT:
                return Direction.UP
        if np.array_equal(self.move, [0, 0, 1]):
            if self.snake.dir == Direction.UP:
                return Direction.LEFT
            if self.snake.dir == Direction.RIGHT:
                return Direction.UP
            if self.snake.dir == Direction.DOWN:
                return Direction.RIGHT
            if self.snake.dir == Direction.LEFT:
                return Direction.DOWN
        assert False

    def post_action(self, score, time_without_score, is_dead):
        if is_dead:
            reward = -10
        elif score > self.score:
            reward = 10
        else:
            reward = 0

        self.score = score
        state_new = self.get_state()
        self.train_short_memory(self.state_old, self.move, reward, state_new,
                                is_dead)
        self.remember(self.state_old, self.move, reward, state_new, is_dead)

    def post_game_over(self, record):
        self.n_games += 1
        self.train_long_memory()
        if self.score > record:
            self.model.save()
