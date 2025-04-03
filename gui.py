from game import Game
from math import ceil, log2
from random import choice
import pygame
import sys

# Constants
DEPTH = ceil(log2(3000))
DEFAULT_ALGORITHM = "minimax"

valid = list(range(20_000, 30_001, 12)) # ensure divisibility by 2, 3 and 4

AVAILABLE_NUMBERS = []
def gen_available():
    global AVAILABLE_NUMBERS
    AVAILABLE_NUMBERS = [choice(valid) for _ in range(5)]

gen_available()


# Initialize Pygame
pygame.init()


# Set up the window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game for AI course")


# Some text stuff
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)
make_black_text = lambda text: font.render(text, True, (0, 0, 0))
make_white_text = lambda text: font.render(text, True, (255, 255, 255))


# Decorator to display the window
def pygame_window(func):
    def wrapper(*args, **kwargs):
        window.fill((255, 255, 255))
        func(*args, **kwargs)
        pygame.display.update()
    return wrapper


# Function to display the entry screen
# Function to display the entry screen
@pygame_window
def entry_screen(number, algorithm, player_moves):
    start = make_black_text("Select number and press ENTER")
    welcome = make_black_text("Welcome to The Game for AI course practical work 1")
    available_numbers = make_black_text(f"Available numbers: {AVAILABLE_NUMBERS}")
    number = make_black_text(f"Select number: {number}")
    algorithm = make_black_text(f"Select algorithm: {'Minimax (M <-> A)' if algorithm == 'minimax' else 'Alpha-Beta (M <-> A)'}")
    player = make_black_text(f"Player moves first: {'Yes (P <-> B)' if player_moves else 'No (P <-> B)'}")

    window.blit(start,             (50, 210))
    window.blit(welcome,           (100, 50))
    window.blit(available_numbers, (100, 300))
    window.blit(number,            (100, 350))
    window.blit(algorithm,         (100, 400))
    window.blit(player,            (100, 450))



# Function to display the game screen
@pygame_window
def game_screen(game: Game, ai_last_move: int | None):
    player_score = make_black_text(f"Player: {game.player}")
    ai_bot_score = make_black_text(f"AI bot: {game.ai_bot}")
    number = make_black_text(f"Number: {game.number}")
    bank = make_black_text(f"Bank: {game.bank}")
    last_move = make_black_text(f"AI's last move: {ai_last_move}")

    window.blit(player_score, (50, 50))
    window.blit(ai_bot_score, (50, 100))
    window.blit(number, (50, 150))
    window.blit(bank, (50, 200))

    if ai_last_move:
        window.blit(last_move, (50, 250))


# Function to display end game screen
@pygame_window
def end_game_screen(player_score, ai_bot_score):
    # Winner text
    if player_score > ai_bot_score:
        winner = make_black_text(f"Winner: Player")
    elif player_score < ai_bot_score:
        winner = make_black_text(f"Winner: AI bot")
    else:
        winner = make_black_text(f"It's a draw!")

    # Score text
    player_score = make_black_text(f"Player score: {player_score}")
    ai_bot_score = make_black_text(f"AI bot score: {ai_bot_score}")

    # Other texts
    game_over = make_black_text("GAME OVER")
    play_again = make_white_text("Play Again (R)")
    quit = make_white_text("Quit (Q)")

    # Buttons background
    pygame.draw.rect(window, BLACK, (200, 400, 200, 50))
    pygame.draw.rect(window, BLACK, (400, 400, 200, 50))

    # Display texts
    window.blit(game_over, (300, 200))
    window.blit(winner, (300, 250))
    window.blit(player_score, (300, 300))
    window.blit(ai_bot_score, (300, 350))
    window.blit(play_again, (210, 410))
    window.blit(quit, (450, 410))


# Function to simulate the game
def play_game(number, algorithm, player_moves):
    game = Game(number)
    algorithms = {"minimax": game.minimax, "alpha-beta": game.alpha_beta}
    move = None
    while game:
        game_screen(game, move)
        if player_moves:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if (event.type == pygame.KEYDOWN and
                    event.key in (pygame.K_2, pygame.K_3, pygame.K_4)):
                    game.make_player_move(int(chr(event.key)))
                    player_moves = not player_moves
        else:
            _, move = algorithms[algorithm](DEPTH)

            if move is None:
                move = 2
                print("SOMETHING WENT VERY WRONG HERE, but selected value 2 as default")

            game.make_ai_bot_move(move)

            player_moves = not player_moves

    player_score, ai_bot_score = game.player.points, game.ai_bot.points
    player_score = game.player.points + (game.bank if not player_moves else 0)
    ai_bot_score = game.ai_bot.points + (game.bank if player_moves else 0)
    return player_score, ai_bot_score



number = ""
algorithm = DEFAULT_ALGORITHM
player_moves = True

while True:
    entry_screen(number, algorithm, player_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if (num := event.unicode).isdigit():
                number += num

            elif event.key == pygame.K_BACKSPACE:
                number = number[:-1]

            elif event.key == pygame.K_m:
                algorithm = "minimax"

            elif event.key == pygame.K_a:
                algorithm = "alpha-beta"

            elif event.key == pygame.K_p:
                player_moves = True

            elif event.key == pygame.K_b:
                player_moves = False

            elif event.key == pygame.K_r:
                gen_available()

            elif event.key == pygame.K_RETURN:
                try:
                    num = int(number)
                    if num not in AVAILABLE_NUMBERS:
                        continue
                except ValueError:
                    continue

                player_score, ai_bot_score = play_game(num, algorithm, player_moves)
                end_game_screen(player_score, ai_bot_score)

                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if (event.type == pygame.QUIT or
                            event.type == pygame.KEYDOWN and
                            event.key == pygame.K_q):
                            pygame.quit()
                            sys.exit()

                        if (event.type == pygame.KEYDOWN and
                            event.key == pygame.K_r):
                            number = ""
                            waiting_for_input = False
