import pygame
import argparse
from snake.game import WIDTH, HEIGHT, WHITE, Snake, Board
from snake.agents import RLAgent, CollisionAwareBot, AwareBot, Human, NotSoBrightBot, AgentType

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    FPS = 500

    parser = argparse.ArgumentParser()
    parser.add_argument('--type',
                        default=AgentType.HUMAN,
                        type=AgentType,
                        choices=[t.value for t in AgentType])
    args = parser.parse_args()

    max_score = 0

    agent = None
    snake = None
    board = None
    if args.type == AgentType.HUMAN:
        agent = Human(snake, board)
    elif args.type == AgentType.NOT_SO_BRIGHT:
        agent = NotSoBrightBot(snake, board)
    elif args.type == AgentType.AWARE:
        agent = AwareBot(snake, board)
    elif args.type == AgentType.COLLISION_AWARE:
        agent = CollisionAwareBot(snake, board)
    elif args.type == AgentType.RL_TRAIN:
        agent = RLAgent(snake, board)

    for i in range(1000):
        board = Board()
        snake = Snake()
        agent.snake = snake
        agent.board = board

        time_without_score = 0
        while True:
            direction = agent.get_action()
            score = snake.score
            if not snake.is_dead:
                snake.update(direction, board)

            time_without_score += 1
            if snake.score > score:
                time_without_score = 0

            if time_without_score >= 10000:
                snake.is_dead = True

            agent.post_action(snake.score, snake.is_dead)

            if snake.is_dead:
                agent.post_game_over(max_score)
                max_score = max(snake.score, max_score)
                print(f'Dead agent: {agent}, score: {snake.score}, max_score: {max_score}')
                break
            board.draw(screen)
            snake.draw(screen)

            font = pygame.font.SysFont('times new roman', 20)
            if snake.is_dead:
                score_surface = font.render('Game over', True, WHITE)
            else:
                score_surface = font.render('Score : ' + str(snake.score), True,
                                            WHITE)
            score_rect = score_surface.get_rect()
            score_rect.topleft = (10, 10)
            screen.blit(score_surface, score_rect)

            pygame.display.update()
            # clock.tick(FPS)

    print(f'Max score for {agent} is {max_score}')
