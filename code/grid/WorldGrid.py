from SimpleGrid import SimpleGrid 
from Tkinter import Tk
import math
import json

class WorldGrid(SimpleGrid):

	def __init__(self,parent,props,map):
		self.map = map
		self.robotCol = -1
		self.robotRow = -1
		self.robotXDev = 0.30
		self.robotYDev = 0.30
		self.robot = 0
		self.callBackList = list()
		SimpleGrid.__init__(self,parent,props)
		
		# mapSquares contains references to the actual 
		# rectangles in the map
		self.mapSquares = list()
		for i in range(0,self.nRows):
			row = list()
			for j in range(0,self.nCols):
				row.append(0)
			self.mapSquares.append(row)
                
		
	def registerCallBack(self,func):
		self.callBackList.append(func)
		
	def drawSquare(self,row,col):
		sqX = self.gridX + (self.gridSqWidth*col)
		sqY = self.gridY + (self.gridSqHeight*row)
		fillstr = ''
		if(self.map.isWall(row,col)):
			fillstr = 'black'
		else:
			fillstr = 'white'
			
		self.mapSquares[row][col] = self.canvas.create_rectangle(sqX, sqY,
					     sqX + self.gridSqWidth,
                         sqY + self.gridSqHeight,
					     outline="black",
					     fill=fillstr)

	def shadeSquare(self,row,col,fillstr):

		if(self.map.isValidSquare(row,col) == False):
			return
				
		sqX = self.gridX + (self.gridSqWidth*col)
		sqY = self.gridY + (self.gridSqHeight*row)

		self.canvas.delete(self.mapSquares[row][col])

		self.canvas.create_rectangle(sqX, sqY,
					     sqX + self.gridSqWidth,
                         sqY + self.gridSqHeight,
                    	 outline="black",
		                 fill=fillstr)
						 
	def enableEvents(self):
		self.canvas.bind("<Button-1>",self.button1Click)
		
	def button1Click(self,event):
		for i in range(len(self.callBackList)):
			self.callBackList[i](event)


	def drawRobot(self,row,col):

		if(self.map.isValidSquare(row,col) == False):
			return

		# erase the last square
		if(self.robot!=0):
			self.canvas.delete(self.robot)
		self.robotCol = col
		self.robotRow = row

		# draw the robot here...
		sqX = self.gridX + (self.gridSqWidth * col)
		sqY = self.gridY + (self.gridSqHeight * row)
		xOffset = self.gridSqWidth * self.robotXDev
		yOffset = self.gridSqHeight * self.robotYDev
		self.robot = self.canvas.create_oval(sqX + xOffset,
								sqY + yOffset,
								(sqX + self.gridSqWidth) - xOffset,
								(sqY + self.gridSqHeight) - yOffset,
														fill="blue")
		
		
		
		
		
def main():
	
	root = Tk()

	props = json.load(open("WorldMap.props"))
	
	sg = WorldGrid(root,props)
	sg.draw()
	root.geometry(props["windowDimensions"])
	root.mainloop()
	
if __name__ == '__main__':
	main()
