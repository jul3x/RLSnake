from snake.game import Direction
from .agent import Agent


class AwareBot(Agent):
    def __init__(self, snake, board):
        super().__init__(snake, board)

    def get_action(self):
        diff_x = self.board.food[0] - self.snake.pos[0][0]
        diff_y = self.board.food[1] - self.snake.pos[0][1]

        direction = None

        should_move_horizontally = False
        if abs(diff_x) >= abs(diff_y):
            should_move_horizontally = True
            direction = Direction.RIGHT if diff_x > 0 else Direction.LEFT
        else:
            direction = Direction.DOWN if diff_y > 0 else Direction.UP

        if direction.is_opposite(self.snake.dir):
            # Make turn
            if should_move_horizontally:
                direction = Direction.DOWN if diff_y > 0 else Direction.UP
            else:
                direction = Direction.RIGHT if diff_x > 0 else Direction.LEFT

        return direction

