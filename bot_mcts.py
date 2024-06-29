import numpy as np
import random as rand

class Node:
	def __init__(self, parent=None, move=None):
		self.parent = parent
		self.children = []
		self.move = move
		self.value = 0
		self.visits = 0
		self.uct = 0

class BotMCTS:
	def __init__(self):
		self.eval = None

	def calc_eval(best_node, self):
		win_rate = best_node.value / best_node.visits
		return round((win_rate + 1) / 2, 2)

	def calc_uct(self, node, exploration_const):
		win_rate = node.value / node.visits
		return win_rate + exploration_const * np.sqrt(np.log(node.parent.visits) / node.visits)

	def select_child(self, node):
		best_children = []
		best_uct = -np.inf
		for child in node.children:
			child.uct = self.calc_uct(child, 1.41)
			if child.uct > best_uct:
				best_children.clear()
				best_children.append(child)
				best_uct = child.uct
			elif child.uct == best_uct:
				best_children.append(child)
		return rand.choice(best_children)

	def expand(self, board, node):
		legal_moves = board.get_legal_moves()
		for child in node.children:
			legal_moves.remove(child.move)
		child_node = Node(parent=node, move=rand.choice(legal_moves))
		child_node.visits = 1
		node.children.append(child_node)
		board.make_move(child_node.move)
		return child_node

	def rollout(self, board):
		legal_moves = board.get_legal_moves()
		if len(legal_moves) > 0:
			move = rand.choice(legal_moves)
			board.make_move(move)
			win_value = -self.rollout(board)
			board.undo_move(move)
		else:
			if board.get_winner() == "No one":
				win_value = 0
			else:
				win_value = 1
		return win_value

	def backprop(self, board, node, rollout_result):
		win_value = rollout_result
		while node.parent != None:
			node.value += win_value
			board.undo_move(node.move)
			node = node.parent
			win_value = -win_value

	def get_move(self, board, num_iterations):
		root_node = Node()
		for iteration in np.arange(num_iterations):
			# selection
			node = root_node
			node.visits += 1
			legal_moves = board.get_legal_moves()
			while len(legal_moves) > 0 and len(node.children) == len(legal_moves):
				node = self.select_child(node)
				node.visits += 1
				board.make_move(node.move)
				legal_moves = board.get_legal_moves()
			if len(legal_moves) > 0:
				# expansion
				node = self.expand(board, node)
				# simulation
				win_value = self.rollout(board)
			else:
				if board.get_winner() == "No one":
					win_value = 0
				else:
					win_value = 1
			# backpropagation
			self.backprop(board, node, win_value)
		best_child = None
		most_visits = 0
		for child in root_node.children:
			if child.visits > most_visits:
				best_child = child
				most_visits = child.visits
		self.eval = self.calc_eval(best_child)
		return best_child.move