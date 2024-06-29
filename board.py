# get_ply()					integer: returns the number of moves played so far					fast
# get_game_state()			tuple: returns the current game state								fast
# show_board()				None: prints the board to the console								slow
# swap_turn()				None: swaps turns without changing the board state					fast
# get_turn()				string: returns either "X" or "O"									fast
# get_winner()				string: returns either "X", "O", or "No one"						medium
# get_legal_moves()			list: returns a list of legal moves or None if the game is over		medium
# make_move(tuple: move)	None: changes the current board state and swaps turns				fast
# undo_move(tuple: move)	None: changes the current board state and swaps turns				fast

import os

class Board:
	def __init__(self):
		self.bitboards = [0, 0, 0]
		self.turn = 1
		self.ply = 0

		self.win_masks = [292, 146, 73, 448, 56, 7, 273, 84]

	def get_ply(self):
		return self.ply

	def get_game_state(self):
		return tuple(self.bitboards)

	def show_board(self):
		board = [["-", "-", "-"],
				 ["-", "-", "-"],
				 ["-", "-", "-"]]

		for row in range(3):
			for col in range(3):
				slot_idx = 8 - (row * 3) - col
				if self.bitboards[1] & (1 << slot_idx) > 0:
					board[row][col] = "X"
				elif self.bitboards[-1] & (1 << slot_idx) > 0:
					board[row][col] = "O"

		os.system("clear")
		print("  1 2 3")
		for row in range(3):
			print(row + 1, board[row][0], board[row][1], board[row][2])

	def swap_turn(self):
		self.turn = -self.turn

	def get_turn(self):
		if self.turn == 1:
			return "X"
		return "O"

	def get_winner(self):
		for mask in self.win_masks:
			if mask & ~self.bitboards[1] == 0:
				return "X"
			if mask & ~self.bitboards[-1] == 0:
				return "O"

		return "No one"

	def get_legal_moves(self):
		if self.get_winner() != "No one":
			return None

		legal_moves = []
		for row in range(3):
			for col in range(3):
				slot_idx = 8 - (row * 3) - col
				if self.bitboards[0] & (1 << slot_idx) == 0:
					legal_moves.append((row + 1, col + 1))

		if len(legal_moves) == 0:
			return None

		return legal_moves

	def make_move(self, move):
		row, col = move
		slot_idx = 8 - ((row - 1) * 3) - (col - 1)
		self.bitboards[self.turn] |= 1 << slot_idx
		self.bitboards[0] = self.bitboards[-self.turn] | self.bitboards[self.turn]
		self.turn = -self.turn
		self.ply += 1

	def undo_move(self, move):
		row, col = move
		slot_idx = 8 - ((row - 1) * 3) - (col - 1)
		self.bitboards[-self.turn] ^= 1 << slot_idx
		self.bitboards[0] = self.bitboards[-self.turn] | self.bitboards[self.turn]
		self.turn = -self.turn
		self.ply -= 1