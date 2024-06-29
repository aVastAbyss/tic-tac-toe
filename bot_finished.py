import numpy as np
import time
import random

class Bot:
	def __init__(self):
		self.nodes_visited = 0
		self.eval = 0
		self.search_time = 0

		self.transposition_table = {}

	def get_ordered_moves(self, board):
		legal_moves = board.get_legal_moves()
		if legal_moves == None:
			return None

		center_move = []
		corner_moves = []
		edge_moves = []
		for move in legal_moves:
			if move == (2, 2):
				center_move.append(move)
			elif move in [(1, 1), (1, 3), (3, 1), (3, 3)]:
				corner_moves.append(move)
			else:
				edge_moves.append(move)

		return center_move + corner_moves + edge_moves

	def negamax(self, board, alpha, beta):
		self.nodes_visited += 1
		legal_moves = self.get_ordered_moves(board)

		if legal_moves == None:
			if board.get_winner() == "No one":
				return 0
			return -1

		game_state = board.get_game_state()
		if game_state in self.transposition_table:
			eval, lower_bound, upper_bound = self.transposition_table[game_state][0:3]
			if eval > lower_bound and eval < upper_bound:
				return eval
			if eval >= upper_bound and eval >= beta:
				return eval
			if eval <= lower_bound and eval <= alpha:
				return eval

		eval = -1
		bounds = [alpha, beta]
		for move in legal_moves:
			board.make_move(move)
			eval = max(eval, -self.negamax(board, -beta, -alpha))
			alpha = max(alpha, eval)
			board.undo_move(move)
			if eval >= beta:
				break

		self.transposition_table[game_state] = [eval, bounds[0], bounds[1]]
		return eval

	def get_move(self, board):
		if board.get_ply() == 0:
			return random.choice([(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)])

		start_time = time.time()
		self.nodes_visited = 0
		self.transposition_table.clear()

		legal_moves = self.get_ordered_moves(board)
		eval_array = np.zeros(len(legal_moves))

		alpha = -1
		beta = 1
		eval = -1

		idx = 0
		for move in legal_moves:
			board.make_move(move)
			eval = max(eval, -self.negamax(board, -beta, -alpha))
			alpha = max(alpha, eval)
			eval_array[idx] = eval
			board.undo_move(move)
			idx += 1

		self.eval = eval
		self.search_time = round((time.time() - start_time) * 1000)
		return legal_moves[eval_array.argmax()]