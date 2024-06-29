import random

class Player:
	def __init__(self):
		self.side = random.choice(["X", "O"])

	def get_move(self):
		valid_numbers = ["1", "2", "3"]
		row = input("Enter a valid row number: ")
		col = input("Enter a valid column number: ")

		if row not in valid_numbers:
			return None
		if col not in valid_numbers:
			return None
		return (int(row), int(col))