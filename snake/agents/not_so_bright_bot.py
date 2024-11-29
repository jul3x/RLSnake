import random
from snake.game import Direction
from .agent import Agent


class NotSoBrightBot(Agent):
    def __init__(self, snake, board):
        super().__init__(snake, board)

    def get_action(self):
        direction = random.choices(list(Direction))
        return direction[0]
