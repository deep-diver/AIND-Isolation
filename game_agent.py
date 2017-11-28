"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = game.get_legal_moves(player)
    my_pos = game.get_player_location(player)

    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)

    base_score = float(len(my_moves) - len(opponent_moves))

    if my_pos in opponent_moves and len(my_moves) > 1:
        base_score = base_score + 2

    return base_score


def custom_score_2(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_pos = game.get_player_location(player)
    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)

    if my_pos in opponent_moves:
        return float(1)
    else:
        return float(0)


def custom_score_3(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = game.get_legal_moves(player)
    my_pos = game.get_player_location(player)

    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)

    base_score = float(len(my_moves) - len(opponent_moves))

    if my_pos in opponent_moves:
        base_score = base_score + 2


    return base_score


class IsolationPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score_3, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def terminal_test(self, game):
        if len(game.get_legal_moves()) is 0:
            return True
        else:
            return False

    def min_value(self, game, depth, curDepth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(game) or depth <= curDepth:
            return self.score(game, self)

        v = float("inf")
        for move in game.get_legal_moves():
            nextGame = game.forecast_move(move)
            v = min(v, self.max_value(nextGame, depth, curDepth+1))
        return v

    def max_value(self, game, depth, curDepth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(game) or depth <= curDepth:
            return self.score(game, self)

        v = float("-inf")
        for move in game.get_legal_moves():
            nextGame = game.forecast_move(move)
            v = max(v, self.min_value(nextGame, depth, curDepth+1))
        return v

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        v = float("-inf")
        moves = (-1, -1)

        for move in game.get_legal_moves():
            nextGame = game.forecast_move(move)
            nextGameScore = self.min_value(nextGame, depth, 1)

            if v < nextGameScore:
                v = nextGameScore
                moves = move

        # print(game.to_string())
        # print(self.score(game, self))
        return moves


class AlphaBetaPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
        self.time_left = time_left
        best_move = (-1, -1)

        try:
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def cutoff_test(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if not game.get_legal_moves():
            return True
        if depth == 0:
            return True

    def min_value(self, game, alpha, beta, depth):
        if self.cutoff_test(game, depth):
            return self.score(game, self)

        v = float("inf")
        for move in game.get_legal_moves():
            nextGame = game.forecast_move(move)
            v = min(v, self.max_value(nextGame, alpha, beta, depth-1))

            if v <= alpha:
                return v

            beta = min(beta, v)
        return v

    def max_value(self, game, alpha, beta, depth):
        if self.cutoff_test(game, depth):
            return self.score(game, self)

        v = float("-inf")
        for move in game.get_legal_moves():
            nextGame = game.forecast_move(move)
            v = max(v, self.min_value(nextGame, alpha, beta, depth-1))

            if v >= beta:
                return v

            alpha = max(alpha, v)
        return v

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if not game.get_legal_moves():
            return (-1, -1)

        v = float("-inf")
        moves = game.get_legal_moves()[0]

        for move in game.get_legal_moves():
            nextGame = game.forecast_move(move)
            nextGameScore = self.min_value(nextGame, alpha, beta, depth-1)

            if v < nextGameScore:
                v = nextGameScore
                moves = move

            alpha = max(alpha, nextGameScore)

        return moves
