from utils import ask_range, ask_in
from random import choice
from game import Game
from time import time

valid = list(range(20_000, 30_001, 12)) # ensure divisibility by 2, 3 and 4
numbers = [choice(valid) for _ in range(5)]

print(numbers)
number = int(ask_in("> Enter number: ", numbers))
game = Game(number)

player_moves = ask_in("> Who goes first? (P)layer or (A)I bot: ", ('p', 'a'))
algorithm = ask_in("> Choose algorithm: (M)inimax or (A)lpha-beta: ", ('m', 'a'))
depth = int(ask_range("> Enter search depth (1-15): ", 1, 15))

player_moves = (player_moves == 'p')
algorithm = {'m': game.minimax,
             'a': game.alpha_beta}[algorithm]

# Game loop
times = []
while game:
    print()
    print(f"=====================")
    print(f"| Number: {game.number}")
    print(f"| Player: {game.player}")
    print(f"| AI bot: {game.ai_bot}")
    print(f"| Bank: {game.bank}")

    if player_moves:
        move = ask_range("> Enter divisor (2, 3, 4): ", 2, 4)
        game.make_player_move(move)

    else:
        start = time()
        _, move = algorithm(depth)
        end = time()
        times.append(end - start)

        if move is None:
            move = 2
            print("SOMETHING WENT VERY WRONG HERE, but selected value 2 as default")

        game.make_ai_bot_move(move)

        print(f"* AI bot moves: {move}")

    player_moves = not player_moves


# Final scores
player_score, ai_bot_score = game.player.points, game.ai_bot.points
player_score = game.player.points + (game.bank if not player_moves else 0)
ai_bot_score = game.ai_bot.points + (game.bank if player_moves else 0)

print(f"Player score: {player_score}")
print(f"AI bot score: {ai_bot_score}")

if player_score > ai_bot_score:
    print("Player wins!")

elif player_score < ai_bot_score:
    print("AI bot wins!")

else:
    print("It's a draw!")

print("Times spent thinking:", times)
print("Average:", sum(times) / len(times))
