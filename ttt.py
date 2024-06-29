from board import Board
from player import Player
from bot_finished import Bot

board = Board()
player = Player()
bot = Bot()

def main():
	while board.get_legal_moves():
		move = None
		legal_moves = board.get_legal_moves()
		while move not in legal_moves:
			board.show_board()
			print(board.get_turn() + "'s turn to play")

			if board.get_turn() == player.side:
				print("Bot eval:", bot.eval)
				print(f"{bot.nodes_visited} nodes searched in {bot.search_time} ms")
				move = player.get_move()
			else:
				move = bot.get_move(board)
				if move not in legal_moves:
					print("Illegal move:", move)
					exit()

		board.make_move(move)

	board.show_board()
	print(board.get_winner(), "won the game!")

main()