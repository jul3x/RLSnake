import pygame
import argparse
from snake.game import WIDTH, HEIGHT, WHITE, Snake, Board
from snake.agents import AgentType

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    parser = argparse.ArgumentParser()
    parser.add_argument('--type',
                        default=AgentType.HUMAN,
                        type=AgentType,
                        choices=[t.value for t in AgentType])
    parser.add_argument('--fps', default=30, type=int)
    parser.add_argument('--n-games', default=1, type=int)
    args = parser.parse_args()

    max_score = 0

    agent = None
    snake = Snake()
    board = Board()
    agent = args.type.get_agent_type()(snake, board)

    MAX_TIME_WITHOUT_SCORE = 1000  # idle protection

    for i in range(args.n_games):
        board = Board()
        snake = Snake()
        agent.snake = snake
        agent.board = board

        time_without_score = 0
        while True:
            if not args.type != AgentType.HUMAN:
                for event in pygame.event.get():
                    pass

            direction = agent.get_action()
            score = snake.score
            if not snake.is_dead:
                snake.update(direction, board)

            time_without_score += 1
            if snake.score > score:
                time_without_score = 0

            if time_without_score >= MAX_TIME_WITHOUT_SCORE:
                snake.is_dead = True

            agent.post_action(snake.score, time_without_score, snake.is_dead)

            if snake.is_dead:
                agent.post_game_over(max_score)
                max_score = max(snake.score, max_score)
                print(
                    f'Game: {agent.n_games}, Score: {snake.score}, Record: {max_score}'
                )
                break
            board.draw(screen)
            snake.draw(screen)

            font = pygame.font.SysFont('times new roman', 20)
            if snake.is_dead:
                score_surface = font.render('Game over', True, WHITE)
            else:
                score_surface = font.render(f'Score: {snake.score}', True,
                                            WHITE)
            score_rect = score_surface.get_rect()
            score_rect.topleft = (10, 10)
            screen.blit(score_surface, score_rect)

            pygame.display.update()
            clock.tick(args.fps)

    print(f'Max score for {args.type} is {max_score}')
