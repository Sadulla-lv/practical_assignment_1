from dataclasses import dataclass

@dataclass
class Player:
    points: int = 0


@dataclass
class GameTreeNode:
    value: int
    player_score: int
    ai_bot_score: int
    is_player: bool
    bank: int

    children: dict[int, "GameTreeNode"] | None = None


class Game:
    def __init__(self, number: int) -> None:
        self.number = number
        self.player = Player()
        self.ai_bot = Player()
        self.bank = 0

    def heuristic_eval(self, node: GameTreeNode) -> float:
        # score difference parameter
        S = node.ai_bot_score - node.player_score

        # bank paramater, when number is less (game is closer to end) it matters more
        B = node.bank * 10 / node.value

        # immediate gain potential (sum of all +1 and -1 directly from given node)
        G = sum(
            (c.ai_bot_score - c.ai_bot_score) - (c.player_score - node.player_score)
            for c in (node.children or {}).values()
        )

        # bank increment potential
        I = len([
            1
            for c in (node.children or {}).values() 
            if c.value % 5 == 0
        ])

        # end game potential, reward for ending game and taking bank
        E = (
            (-1 if node.is_player else 1) * max([
                c.bank + (-1 if c.value % 2 == 0 else 1)
                for c in node.children.values()
            ])
            if node.children and node.value // 4 <= 10
            else 0
        )

        # weighted sum
        return 10 * S + B + 3 * G + 5 * I + 10 * E


    # calculate and commit a move
    def make_move(self, current: Player, divisor: int) -> None:
        self.number //= divisor
        self.bank += (0, 1)[self.number % 5 == 0]
        current.points += (1, -1)[self.number % 2 == 0]


    # generate game tree
    def game_tree(self, current: Player, depth: int) -> tuple[GameTreeNode, int]:
        def _subtree(
            number: int,
            player_score: int,
            ai_bot_score: int,
            is_player: bool,
            bank: int,
            depth: int
        ) -> tuple[GameTreeNode, int]:
            node = GameTreeNode(number, player_score, ai_bot_score, is_player, bank)
            node_count = 1

            # stop recursion when depth limit is reached or number is small
            if depth == 0 or number <= 10:
                return node, node_count

            node.children = {}

            # moves by dividing by 2, 3 and 4
            for d in (2, 3, 4):
                new_number = number // d

                # update player or ai bot score (even/odd rule)
                score_change = (1, -1)[new_number % 2 == 0]
                new_player = player_score + (score_change if is_player else 0)
                new_ai_bot = ai_bot_score + (score_change if not is_player else 0)

                # update bank (number ending on 0 or 5, which is divisibility by 5 rule)
                new_bank = bank + (0, 1)[new_number % 5 == 0]
                child, child_count = _subtree(new_number, new_player, new_ai_bot, not is_player, new_bank, depth - 1)

                node_count += child_count

                node.children[d] = child

            return node, node_count

        return _subtree(self.number, self.player.points, self.ai_bot.points, current is self.player, self.bank, depth)


    # minimax algorithm implementation
    def minimax(
        self,
        depth: int,
        is_maximizing: bool = True
    ) -> tuple[float, int | None]:
        def _minimax(
            node: GameTreeNode,
            depth: int,
            is_maximizing: bool
        ) -> tuple[float, int | None]:
            # base case, stop if depth is zero or no further moves exist
            if depth == 0 or node.children is None:
                return self.heuristic_eval(node), None

            best_move = None
            best_value = float('-inf') if is_maximizing else float('inf')

            # iterate through all possible moves
            for divisor, child_node in node.children.items():
                child_value, _ = _minimax(child_node, depth - 1, not is_maximizing)

                # maximize or minimize based on whose turn it is
                if (is_maximizing and child_value > best_value) or (not is_maximizing and child_value < best_value):
                    best_value = child_value
                    best_move = divisor

            return best_value, best_move

        # generate game tree and start minimax
        root, nodes = self.game_tree(self.ai_bot, depth)
        print("Nodes generated:", nodes)
        return _minimax(root, depth, is_maximizing)


    # alpha-beta pruning algorithm implementation
    def alpha_beta(
        self,
        depth: int,
        is_maximizing: bool = True
    ) -> tuple[float, int | None]:
        def _alpha_beta(
            node: GameTreeNode,
            alpha: float,
            beta: float,
            depth: int,
            is_maximizing: bool
        ) -> tuple[float, int | None]:
            # base case, stop if depth is zero or no further moves exist
            if depth == 0 or node.children is None:
                return self.heuristic_eval(node), None

            best_move = None

            # iterate through all possible moves
            for divisor, child_node in node.children.items():
                child_value, _ = _alpha_beta(child_node, alpha, beta, depth - 1, not is_maximizing)

                # maximize or minimize based on whose turn it is
                if is_maximizing:
                    if child_value > alpha:
                        alpha = child_value
                        best_move = divisor
                else:
                    if child_value < beta:
                        beta = child_value
                        best_move = divisor

                # alpha-beta pruning
                if alpha >= beta:
                    break

            return (beta, alpha)[is_maximizing], best_move

        # generate game tree and start alpha-beta
        root, nodes = self.game_tree(self.ai_bot, depth)
        print("Nodes generated:", nodes)
        return _alpha_beta(root, float('-inf'), float('inf'), depth, is_maximizing)


    # Boilerplate code
    def make_player_move(self, divisor: int) -> None:
        self.make_move(self.player, divisor)

    def make_ai_bot_move(self, divisor: int) -> None:
        self.make_move(self.ai_bot, divisor)

    def __bool__(self) -> bool:
        return self.number > 10
