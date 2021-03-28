import os
# from bricks import
from colorama import init, Fore, Back, Style
init()
class Board:
	
	def __init__(self, rows, columns):
		self.matrix = []
		self.rows = rows
		self.columns = columns

	def create_board(self): # creates the entire grid

		for i in range (self.rows):                              
			self.new = []                 
			for j in range (self.columns): 
				self.new.append(" ")      
			self.matrix.append(self.new)

	def theyllprintit(self,string):
		temp = 0
		for i in range(self.rows):
			if i == 0:
				print(Back.RED + "THE BRICK BREAKER".center(self.columns) + Style.RESET_ALL)
			if i == 0:
				print(Back.BLUE + string.center(self.columns) + Style.RESET_ALL)
			if i == self.rows-1:
				print(Back.GREEN + " ".center(self.columns) + Style.RESET_ALL)
			for j in range(self.columns):
				if self.matrix[i][j] == "X":
					temp = 1
					if self.matrix[i][j+1] == 1:
						print(Fore.BLUE + self.matrix[i][j],end='')
					elif self.matrix[i][j+1] == 2:
						print(Fore.YELLOW + self.matrix[i][j],end='')
					elif self.matrix[i][j+1] == 3:
						print(Fore.GREEN + self.matrix[i][j],end='')
					elif self.matrix[i][j+1] == 5:
						print(Fore.WHITE + self.matrix[i][j],end='')
					elif self.matrix[i][j+1] == -10:
						print(Fore.LIGHTRED_EX + self.matrix[i][j],end='')
					else:
						print(Style.RESET_ALL + " ",end='')
				elif self.matrix[i][j] == "I":
					print(Fore.CYAN + self.matrix[i][j],end='')
				elif self.matrix[i][j] == "o":
					print(Fore.RED + self.matrix[i][j],end='')
				elif self.matrix[i][j] == "<==>":
					print(Style.RESET_ALL + self.matrix[i][j],end='')	
				elif self.matrix[i][j] == "=><=":
					print(Style.RESET_ALL + self.matrix[i][j],end='')
				elif self.matrix[i][j] == ">>":
					print(Style.RESET_ALL + self.matrix[i][j],end='')
				elif self.matrix[i][j] == ".-.":
					print(Style.RESET_ALL + self.matrix[i][j],end='')	
				elif self.matrix[i][j] == "t":
					print(Style.RESET_ALL + self.matrix[i][j],end='')
				else:
					if i == self.rows-1:
						s=2
					if i == 0:
						s=1
					else:
						print(Style.RESET_ALL + " ",end='')
			print(Style.RESET_ALL)
		return temp
