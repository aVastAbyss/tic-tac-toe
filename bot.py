import random

class Bot:
	def __init__(self):
		self.nodes_visited = 0
		self.eval = 0
		self.search_time = 0

	def check_for_win(self, board):
		for move in board.get_legal_moves():
			board.make_move(move)
			if board.get_winner() != "No one":
				winning_move = move
				board.undo_move(move)
				return winning_move

			board.undo_move(move)

	def check_opponent(self, board):
		board.swap_turn()
		for move in board.get_legal_moves():
			board.make_move(move)
			if board.get_winner() != "No one":
				winning_move = move
				board.undo_move(move)
				board.swap_turn()
				return winning_move

			board.undo_move(move)
		board.swap_turn()

	def get_move(self, board):
		if board.get_ply() == 0:
			return (2, 2)

		legal_moves = board.get_legal_moves()
		if board.get_ply() == 1:
			if (2, 2) in legal_moves:
				return (2, 2)
			else:
				return random.choice([(1, 3), (3, 1), (1, 1), (3, 3)])

		our_win_move = self.check_for_win(board)
		their_win_move = self.check_opponent(board)
		if our_win_move:
			return our_win_move
		if their_win_move:
			return their_win_move

		return random.choice(legal_moves)