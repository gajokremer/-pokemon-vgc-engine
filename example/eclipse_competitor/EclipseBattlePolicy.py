from typing import List, Union
from vgc.behaviour import BattlePolicy
from vgc.behaviour.BattlePolicies import BFSNode, game_state_eval
from vgc.datatypes.Constants import DEFAULT_N_ACTIONS
from vgc.datatypes.Objects import GameState

# from vgc.behaviour.BattlePolicies import RandomPlayer, Minimax, BreadthFirstSearch


class EclipseBattlePolicy(BattlePolicy):
    def get_action(self, s: Union[List[float], GameState]) -> int:
        if isinstance(s, list):
            return s.index(max(s))
        elif isinstance(s, GameState):
            return self._determine_action_from_game_state(s)


class MinimaxAlphaBeta(BattlePolicy):
    """
    Tree search algorithm with alpha-beta pruning.
    """

    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth

    def get_action(self, g) -> int:
        def minimax(node, depth, alpha, beta, maximizing_player):
            if depth == 0 or node.is_terminal():
                return game_state_eval(node.g, depth)
            if maximizing_player:
                max_eval = float("-inf")
                best_action = None
                for i in range(DEFAULT_N_ACTIONS):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, alpha, beta, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_action = i
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                if node == root:
                    return best_action
                return max_eval
            else:
                min_eval = float("inf")
                for i in range(DEFAULT_N_ACTIONS):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval

        root = BFSNode()
        root.g = g
        best_action = minimax(root, self.max_depth, float("-inf"), float("inf"), True)
        return best_action


class MinimaxAlphaBetaEnhanced(BattlePolicy):
    """
    Enhanced Tree search algorithm with alpha-beta pruning and better heuristics.
    """

    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth

    def get_action(self, g) -> int:
        def minimax(node, depth, alpha, beta, maximizing_player):
            if depth == 0 or node.is_terminal():
                return game_state_eval(node.g, depth)
            if maximizing_player:
                max_eval = float("-inf")
                best_action = None
                for i in sorted(
                    range(DEFAULT_N_ACTIONS),
                    key=lambda x: move_priority(node, x),
                    reverse=True,
                ):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, alpha, beta, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_action = i
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                if node == root:
                    return best_action
                return max_eval
            else:
                min_eval = float("inf")
                for i in sorted(
                    range(DEFAULT_N_ACTIONS), key=lambda x: move_priority(node, x)
                ):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval

        def game_state_eval(g, depth):
            # Improved heuristic function to evaluate game states
            # Example heuristic: difference in score, weighted by depth
            score = (
                g.get_score()
            )  # Assume get_score returns a score representing the state
            return score - depth

        def move_priority(node, move):
            # Implement a function to prioritize moves
            # Example: prioritize moves that increase player's score
            child = node.create_child(move)
            return game_state_eval(child.g, 0)

        root = BFSNode()
        root.g = g
        best_action = minimax(root, self.max_depth, float("-inf"), float("inf"), True)
        return best_action


class MinimaxAlphaBetaEnhanced2(BattlePolicy):
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.transposition_table = TranspositionTable()

    def get_action(self, g) -> int:
        def iterative_deepening_minimax(root, max_depth):
            best_action = None
            for depth in range(1, max_depth + 1):
                best_action = minimax(root, depth, float("-inf"), float("inf"), True)
            return best_action

        def minimax(node, depth, alpha, beta, maximizing_player):
            state_value = self.transposition_table.lookup(node)
            if state_value is not None:
                return state_value

            if depth == 0 or node.is_terminal():
                return game_state_eval(node.g, depth)

            if maximizing_player:
                max_eval = float("-inf")
                best_action = None
                for i in sorted(
                    range(DEFAULT_N_ACTIONS),
                    key=lambda x: move_priority(node, x),
                    reverse=True,
                ):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, alpha, beta, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_action = i
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                if node == root:
                    return best_action
                self.transposition_table.store(node, max_eval)
                return max_eval
            else:
                min_eval = float("inf")
                for i in sorted(
                    range(DEFAULT_N_ACTIONS), key=lambda x: move_priority(node, x)
                ):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                self.transposition_table.store(node, min_eval)
                return min_eval

        def game_state_eval(g, depth):
            player_score = g.get_player_score()
            opponent_score = g.get_opponent_score()
            score_diff = player_score - opponent_score
            return score_diff - depth * 10

        def move_priority(node, move):
            child = node.create_child(move)
            return game_state_eval(child.g, 0)

        root = BFSNode()
        root.g = g
        best_action = iterative_deepening_minimax(root, self.max_depth)
        return best_action


class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, node):
        return self.table.get(node.state_hash())

    def store(self, node, value):
        self.table[node.state_hash()] = value


class MinimaxDepthLimited(BattlePolicy):
    """
    Minimax with depth limitation and heuristic evaluation.
    """

    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth

    def get_action(self, g) -> int:
        def minimax(node, depth, maximizing_player):
            if depth == 0 or node.is_terminal():
                return game_state_eval(node.g, depth)
            if maximizing_player:
                max_eval = float("-inf")
                best_action = None
                for i in range(DEFAULT_N_ACTIONS):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_action = i
                if node == root:
                    return best_action
                return max_eval
            else:
                min_eval = float("inf")
                for i in range(DEFAULT_N_ACTIONS):
                    child = node.create_child(i)
                    eval = minimax(child, depth - 1, True)
                    min_eval = min(min_eval, eval)
                return min_eval

        root = BFSNode()
        root.g = g
        best_action = minimax(root, self.max_depth, True)
        return best_action
