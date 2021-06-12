
import pygame
from pygame import event
from pygame.constants import KEYDOWN
import random
import time
import threading
import sys

class Board:
	def __init__(self, width:int, height:int):
		self.width = width
		self.height = height
		#0 means dead and 1 means alive
		self.grid = [[random.randint(0, 1) if random.random() * 10 < 1.5 else 0 for i in range(width)] for j in range(height)]

	def __getitem__(self, key):
		return self.grid[key]

	def getNumberOfNeighbours(self, i, j):
		"""
			Returns the number of neighbours for the given index
			Args:
				i, j: horizontal and vertical co-ordinate of the the grid

			Returns:
				count: number of neighbours of the given grid

		"""
		count = 0


		if i > 0 and j > 0:
			if self.grid[i - 1][j - 1]:
				count += 1

		if j > 0:
			if self.grid[i][j - 1]:
				count += 1

		if i < self.width - 1 and j > 0:
			if self.grid[i + 1][j - 1]:
				count += 1

		if i > 0:
			if self.grid[i - 1][j]:
				count += 1

		if i < self.width - 1:
			if self.grid[i + 1][j]:
				count += 1

		if i > 0 and j < self.height - 1:
			if self.grid[i - 1][j + 1]:
				count += 1

		if j < self.height - 1:
			if self.grid[i][j + 1]:
				count += 1
			
		if i < self.width - 1 and j < self.height - 1:
			if self.grid[i + 1][j + 1]:
				count += 1

		return count
			


def init(width, height):
	"""
		Initilize the pygame  
	""" 
	pygame.init()
	screen = pygame.display.set_mode((width, height))

	pygame.display.set_caption("Conway Game of Life")

	return screen


def conwayGameOfLife(board:Board):
	"""
		Game of life screen grid values indicating if the cell is alive or dead
	"""

	for i in range(board.width):
		for j in range(board.height):
			countNeighbours = board.getNumberOfNeighbours(i, j)

			if countNeighbours < 2:
				board[i][j] = 0

			if countNeighbours > 2 and countNeighbours < 4 and board[i][j] == 1:
				board[i][j] = 1

			if countNeighbours > 3:
				board[i][j] = 0

			if countNeighbours == 3 and board[i][j] == 0:
				board[i][j] = 1


	return board


def handleEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()


def run(width, height):
	screen = init(width, height)
	tileNumberHorizontal = 60
	tileNumberVertical = 60

	tileWidth =  width // tileNumberHorizontal
	tileHeight = height // tileNumberVertical


	running = True

	board = Board(tileNumberHorizontal, tileNumberVertical)

	eventThread = threading.Thread(target=handleEvents)
	eventThread.start()

	# game loop
	while running:
		handleEvents()
		
		# render loop
		screen.fill((255, 255, 255))

		for i in range(board.width):
			for j in range(board.height):
				pygame.draw.rect(screen, (120, 120, 120), pygame.Rect(tileWidth * i, tileHeight * j, tileWidth, tileHeight))
				if board[i][j] == 1:
					pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(tileWidth * i, tileHeight * j, tileWidth - 1, tileHeight - 1))
				else:
					pygame.draw.rect(screen, (240, 240, 240), pygame.Rect(tileWidth * i, tileHeight * j, tileWidth - 1, tileHeight - 1))

		board = conwayGameOfLife(board)

		time.sleep(0.2)
    					

		pygame.display.flip()


if __name__ == "__main__":
	run(900, 900)