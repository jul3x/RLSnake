class Agent:

    def __init__(self, snake, board):
        self.snake = snake
        self.board = board
        self.n_games = 0

    def get_action():
        raise NotImplementedError

    def post_action(self, score, time_without_score, is_dead):
        pass

    def post_game_over(self, record):
        self.n_games += 1
