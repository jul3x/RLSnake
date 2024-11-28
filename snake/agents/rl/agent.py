import torch #pytorch
import random
import numpy as np #numpy
from collections import deque #data structure to store memory
from snake.game import Snake, Board, Direction
from .model import Linear_QNet, QTrainer #importing the neural net from step 2
# from .plot import plot #importing the plotter from step 2

MAX_MEMORY = 10_000
BATCH_SIZE = 1000
LR = 0.002 #learning rate

class RLAgent:
    def __init__(self, snake, board):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(12, 1024, 3) #input size, hidden size, output size
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.snake = snake
        self.board = board
        self.score = 0
        self.move = None
        self.state_old = None

    def get_state(self):
        point_l = (self.snake.pos[0][0] - 1, self.snake.pos[0][1])
        point_r = (self.snake.pos[0][0] + 1, self.snake.pos[0][1])
        point_u = (self.snake.pos[0][0], self.snake.pos[0][1] - 1)
        point_d = (self.snake.pos[0][0], self.snake.pos[0][1] + 1)
        dir_l = self.snake.dir == Direction.LEFT
        dir_r = self.snake.dir == Direction.RIGHT
        dir_u = self.snake.dir == Direction.UP
        dir_d = self.snake.dir == Direction.DOWN

        state = [
            (dir_r and self.snake.collision(self.board, point_r)) or # Danger straight
            (dir_l and self.snake.collision(self.board, point_l)) or
            (dir_u and self.snake.collision(self.board, point_u)) or
            (dir_d and self.snake.collision(self.board, point_d)),

            (dir_u and self.snake.collision(self.board, point_r)) or # Danger right
            (dir_d and self.snake.collision(self.board, point_l)) or
            (dir_l and self.snake.collision(self.board, point_u)) or
            (dir_r and self.snake.collision(self.board, point_d)),

            (dir_d and self.snake.collision(self.board, point_r)) or # Danger left
            (dir_u and self.snake.collision(self.board, point_l)) or
            (dir_r and self.snake.collision(self.board, point_u)) or
            (dir_l and self.snake.collision(self.board, point_d)),

            dir_l, #direction
            dir_r,
            dir_u,
            dir_d,

            self.board.food[0] < self.snake.pos[0][0],
            self.board.food[0] > self.snake.pos[0][0],
            self.board.food[1] < self.snake.pos[0][1],
            self.board.food[1] > self.snake.pos[0][1],

            len(self.snake.pos) / (self.board.boundaries * self.board.boundaries)
        ]
        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action_embedding(self, state):
        self.epsilon = 100 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
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

    def post_action(self, score, is_dead):
        if is_dead:
            reward = -10
        elif score > self.score:
            reward = 10
        else:
            reward = 0

        self.score = score
        state_new = self.get_state()
        self.train_short_memory(self.state_old, self.move, reward, state_new, is_dead)
        self.remember(self.state_old, self.move, reward, state_new, is_dead)

    def post_game_over(self, record):
        self.n_games += 1
        self.train_long_memory()
        if self.score > record:
            self.model.save()

        print('Game', self.n_games, 'Score', self.score, 'Record:', record)
