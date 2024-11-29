import pygame
from snake.game import Direction
from .agent import Agent


class Human(Agent):

    def __init__(self, snake, board):
        super().__init__(snake, board)

    def get_action(self):
        direction = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                direction = Direction.by_key(event.key)
        return direction
