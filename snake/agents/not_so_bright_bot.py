import random
from snake.game import Direction


class NotSoBrightBot:
    def __init__(self, snake, board):
        self.snake = snake
        self.board = board

    def get_action(self):
        direction = random.choices(list(Direction))
        return direction[0]
