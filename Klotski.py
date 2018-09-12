import random
import numpy as np 
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import Qt

class Block(QLabel):
	def __init__(self, text):
		super().__init__()

		# Properties of the grids
		self.Text = text
		self.Size = 80
		self.Background = "orange"
		self.ZeroBackground = "gray"
		self.BorderRadius = "10px"

		#properties of text on the block
		self.Font = "Arial"
		self.FontSize = 30
		self.Bold = True
		self.Alignment = "center"
		self.initUI()

	def initUI(self):
		# Block
		self.setFixedSize(self.Size, self.Size)
		# Text
		font = QFont(self.Font, self.FontSize)
		font.setBold(self.Bold)
		self.setFont(font)

		# Set color of text
		pa = QPalette()
		pa.setColor(QPalette.WindowText, Qt.white)
		self.setPalette(pa)
		
		self.setStyleSheet("border-radius:" + self.BorderRadius)
		self.setAlignment(Qt.AlignCenter)

		# If number == 0, block background should be the same as window background
		if self.Text ==0:
			self.setStyleSheet("background-color:%s;" % self.ZeroBackground)
		else:
			self.setText(str(self.Text))
			self.setStyleSheet("background: %s;" % self.Background)


class Puzzle(QWidget):
	
	def __init__(self):
		# Basic stuff of the game
		super().__init__()
		self.Title = 'Puzzle Game'
		# Size of rows and columns
		self.PuzzleSize = 4
		self.background = 'gray'
		# create 2d array with random number from 0 to 15
		self.matrix = self.CreateMatrix()
		# layout of the window
		self.Top = 10
		self.Left = 10
		self.Size = 400

		self.ZeroRow, self.ZeroCol = self.ZeroPos()

		self.layout = QGridLayout()

		self.initUI()
		

	def initUI(self):
		self.setWindowTitle(self.Title)
		self.setGeometry(self.Left,self.Top, self.Size, self.Size)
		self.setStyleSheet("background:" + self.background)
		
		self.SetLayout()

	def CreateMatrix(self):
		
		# get an array with random int from 0 to 16
		blocks = list(range(0,16))
		# mess around the elements in array to make sure the number is random 
		random.shuffle(blocks)
		# convert 1d array into 2d array
		matrix = [blocks[x:x+4] for x in range(0,len(blocks),4)]

		return matrix

	def ZeroPos(self):
		# find zero in the matrix
		for items in self.matrix: # go through every sub-list
			if 0 in items: 
				zeroRow = self.matrix.index(items) #find out 0 in which sub list
				zeroCol = items.index(0)
		return zeroRow, zeroCol

	def SetLayout(self):
		
		for row in range(4):
			for col in range(4):
				self.layout.addWidget(Block(self.matrix[row][col]), row, col)
		self.setLayout(self.layout)
		self.show()

	def keyPressEvent(self, event):
		key = event.key()

		if (key == Qt.Key_Up or key == Qt.Key_W):
			self.move('up')
		elif (key == Qt.Key_Down or key == Qt.Key_S):
			self.move('down')
		elif (key == Qt.Key_Left or key == Qt.Key_A):
			self.move('left')
		elif (key == Qt.Key_Right or key == Qt.Key_D):
			self.move('right')

	def move(self, direction):
		ZeroRow = self.ZeroRow
		ZeroCol = self.ZeroCol
		if direction == 'up' and self.ZeroRow != 3:
			# swap position of 0 and the one below it
			self.matrix[ZeroRow][ZeroCol], self.matrix[ZeroRow+1][ZeroCol] = self.matrix[ZeroRow+1][ZeroCol], self.matrix[ZeroRow][ZeroCol]
			# update position of zero
			self.ZeroRow += 1

		if direction == 'down' and self.ZeroRow != 0:
			# swap position of 0 and the one below it
			self.matrix[ZeroRow][ZeroCol], self.matrix[ZeroRow-1][ZeroCol] = self.matrix[ZeroRow-1][ZeroCol], self.matrix[ZeroRow][ZeroCol]
			# update position of zero
			self.ZeroRow -= 1

		if direction == 'left' and self.ZeroCol != 3:
			# swap position of 0 and the one below it
			self.matrix[ZeroRow][ZeroCol], self.matrix[ZeroRow][ZeroCol+1] = self.matrix[ZeroRow][ZeroCol+1], self.matrix[ZeroRow][ZeroCol]
			# update position of zero
			self.ZeroCol+= 1

		if direction == 'right' and self.ZeroCol != 0:
			# swap position of 0 and the one below it
			self.matrix[ZeroRow][ZeroCol], self.matrix[ZeroRow][ZeroCol-1] = self.matrix[ZeroRow][ZeroCol-1], self.matrix[ZeroRow][ZeroCol]
			# update position of zero
			self.ZeroCol -= 1

		self.SetLayout()
		# After each move, check if use find the right solution
		# if they do, message box bumps up
		# click ok to restart another game
		if (self.CheckResult()):
			# message box bumps up
			# user click ok to restart the game
			print(self.matrix)
			if QMessageBox.Ok == QMessageBox.information(self, 'Congradulations!', 'You win!!!'):
				self.matrix = self.CreateMatrix()
				self.SetLayout()

	def CheckResult(self):
		# first check if 0 is the last
		if self.matrix[self.PuzzleSize-1][self.PuzzleSize-1] != 0:
			return False
		# check numbers are in right position
		for row in range(self.PuzzleSize):
			for col in range(self.PuzzleSize):
				if self.matrix[row][col] != row * self.PuzzleSize + col + 1:
					# user find the solution
					if row == 3 and col == 3:
						pass
					else:
						print(row,col)
						return False
		
		return True


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Puzzle()
	sys.exit(app.exec_())

		


