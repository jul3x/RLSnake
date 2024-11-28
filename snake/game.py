from enum import Enum
import pygame
import random

WIDTH, HEIGHT = 800, 800
BLOCK_SIZE = 25
OFFSET = 75
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Direction(str, Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'

    @staticmethod
    def by_key(key):
        if key == pygame.K_UP:
            return Direction.UP
        if key == pygame.K_DOWN:
            return Direction.DOWN
        if key == pygame.K_LEFT:
            return Direction.LEFT
        if key == pygame.K_RIGHT:
            return Direction.RIGHT

    def is_opposite(self, dir):
        return (self == Direction.UP and dir == Direction.DOWN) or \
            (self == Direction.DOWN and dir == Direction.UP) or \
            (self == Direction.LEFT and dir == Direction.RIGHT) or \
            (self == Direction.RIGHT and dir == Direction.LEFT)


class Board:

    def __init__(self):
        self.boundaries = 26
        self.food = (10, 12)

    def spawn_food(self):
        self.food = (random.randint(0, self.boundaries - 1),
                     random.randint(0, self.boundaries - 1))

    def draw(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(
            screen, WHITE,
            pygame.Rect(OFFSET - BLOCK_SIZE, OFFSET - BLOCK_SIZE,
                        BLOCK_SIZE * (self.boundaries + 2),
                        BLOCK_SIZE * (self.boundaries + 2)), 25)

        pygame.draw.rect(
            screen, RED,
            pygame.Rect(OFFSET + self.food[0] * BLOCK_SIZE,
                        OFFSET + self.food[1] * BLOCK_SIZE, BLOCK_SIZE,
                        BLOCK_SIZE))


class Snake:

    def __init__(self):
        self.pos = [(5, 6)]
        self.dir = Direction.UP
        self.score = 0
        self.is_dead = False

    @staticmethod
    def get_new_pos(position, direction):
        sign = 1 if direction in (Direction.DOWN, Direction.RIGHT) else -1
        diff = (sign, 0) if direction in (Direction.LEFT,
                                          Direction.RIGHT) else (0, sign)
        new_position = (position[0] + diff[0], position[1] + diff[1])
        return new_position

    @staticmethod
    def move_chain(chain, direction):
        new_position = Snake.get_new_pos(chain[0], direction)
        new_positions = [new_position] + chain[:-1]
        return new_positions

    def move_eat(self, board):
        self.score += 1
        new_position = self.get_new_pos(self.pos[0], self.dir)
        self.pos = [new_position] + self.pos
        board.spawn_food()

    def move(self):
        new_position = self.get_new_pos(self.pos[0], self.dir)
        self.pos = [new_position] + self.pos[:-1]

    def update(self, direction, board):
        if self.collision(board):
            self.is_dead = True
            return False

        if self.dir in (Direction.UP,
                        Direction.DOWN) and direction in (Direction.LEFT,
                                                          Direction.RIGHT):
            self.dir = direction
        if self.dir in (Direction.LEFT,
                        Direction.RIGHT) and direction in (Direction.UP,
                                                           Direction.DOWN):
            self.dir = direction

        if self.get_new_pos(self.pos[0], self.dir) == board.food:
            self.move_eat(board)
        else:
            self.move()
        return True

    def collision(self, board):
        for pos in self.pos[1:]:
            if pos == self.pos[0]:
                return True

        if self.pos[0][0] < 0 or self.pos[0][1] < 0 or self.pos[0][
                0] >= board.boundaries or self.pos[0][1] >= board.boundaries:
            return True

        return False

    def draw(self, screen):
        for pos in self.pos:
            pygame.draw.rect(
                screen, GREEN,
                pygame.Rect(OFFSET + pos[0] * BLOCK_SIZE,
                            OFFSET + pos[1] * BLOCK_SIZE, BLOCK_SIZE,
                            BLOCK_SIZE))
