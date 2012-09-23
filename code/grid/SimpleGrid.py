from Tkinter import Tk, Canvas, Frame, BOTH
import time
import json

class SimpleGrid(Frame):
	
	def __init__(self, parent, props):
		Frame.__init__(self,parent)
		
		self.parent = parent
		self.iWidth = props['width']
		self.iHeight = props['height']
		self.nCols = props['cols']
		self.nRows = props['rows']
		self.gWidthPercent = 0.90
		self.gHeightPercent = 0.90

		self.gridSqWidth = 0
		self.gridSqHeight = 0
		self.gridX = 0
		self.gridY = 0
		
		self.initGrid()
		
	def initGrid(self):
		self.parent.title("SimpleGrid")
		self.pack(fill=BOTH, expand=1)
		self.buildCanvas()
		self.calculateDimensions()
		self.enableEvents()
		
	def calculateDimensions(self):
	
		# calculate the size of the grid squares
		self.gridSqWidth = (self.gWidthPercent * self.iWidth) / self.nCols
		self.gridSqHeight = (self.gHeightPercent * self.iHeight) / self.nRows
	
		# calculate the upper left corner
		self.gridX = (1.0 - self.gWidthPercent) * self.iWidth / 2.0
		self.gridY = (1.0 - self.gHeightPercent) * self.iHeight / 2.0
		
	def buildCanvas(self):
		self.canvas = Canvas(self)
		
	def draw(self):		
		
		for i in range(0,self.nRows):
			for j in range(0,self.nCols):
				self.drawSquare(i,j)
		
		self.canvas.pack(fill=BOTH, expand=1)
		
	def drawSquare(self,row,col):
		sqX = self.gridX + (self.gridSqWidth*col)
		sqY = self.gridY + (self.gridSqHeight*row)
		self.canvas.create_rectangle(sqX, sqY,
									 sqX + self.gridSqWidth,
									 sqY + self.gridSqHeight,
									 outline="black")
		
		
	def enableEvents(self):
		# do nothing -- let child classes do this
		return
		
def main():
	
	root = Tk()

	props = json.load(open("GridProperties.json"))
	
	sg = SimpleGrid(root,props)
	sg.draw()
	root.geometry(props["windowDimensions"])
	root.mainloop()
	
if __name__ == '__main__':
	main()
	
