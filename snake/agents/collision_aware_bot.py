from copy import deepcopy
from snake.game import Direction


class CollisionAwareBot:

    def __init__(self, snake, board):
        self.snake = snake
        self.board = board

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

        if self.is_collision(direction):
            # This will cause collision so we need to rescue ourselves
            for possible_direction in Direction:
                if possible_direction.is_opposite(self.snake.dir):
                    continue

                if not self.is_collision(possible_direction):
                    direction = possible_direction
                    break

        return direction

    def is_collision(self, direction):
        # Simulate behavior and check if collision is possible
        # Copy objects to make sure that the original ones are immutable
        # Maybe not the most elegant way but the fastest to implement
        snake_copy = deepcopy(self.snake)
        board_copy = deepcopy(self.board)
        snake_copy.update(direction, board_copy)
        return not snake_copy.update(direction, board_copy)
