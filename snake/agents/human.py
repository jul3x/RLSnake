import pygame
from snake.game import Direction


class Human:
    def __init__(self, snake, board):
        self.snake = snake
        self.board = board

    def get_action(self):
        direction = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                direction = Direction.by_key(event.key)
        return direction
