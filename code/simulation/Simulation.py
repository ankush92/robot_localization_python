import sys

sys.path.append("./grid")
sys.path.append("./robot")
sys.path.append("./map")

from WorldGrid import WorldGrid
from Robot import Robot
from Tkinter import Tk
from WorldMap import WorldMap
import random
import json
import math


class Simulation:

	def __init__(self,propsfile):
		self.canvas = Tk()
		
		self.props = json.load(open(propsfile))
		self.worldMap = WorldMap(propsfile)
		
		self.wg = WorldGrid(self.canvas,self.props,self.worldMap)
		self.wg.registerCallBack(self.processEvent)
		
		self.robot = Robot(self.props,self.worldMap)
		self.robot.registerSenseCallBack(self.sense)
		self.robot.registerMoveCallBack(self.move)
		
		self.rRow = -1
		self.rCol = -1

		self.randomizeRobotPosition()
		self.robot.sense()
		self.shadeSquares()
		
	def randomizeRobotPosition(self):
		# randomly select the starting robot location --
		# do this until a valid square (i.e., not a wall) is 
		# selected
		found = False
		while (found == False):
			row = random.randint(0,self.worldMap.nRows-1)
			col = random.randint(0,self.worldMap.nCols-1)
			if(self.worldMap.isValidSquare(row,col)):
				found = True
				self.rRow = row
				self.rCol = col


	def move(self,dirc):
		
		row = self.rRow
		col = self.rCol
		if(dirc == 1):	# NORTH
			row -= 1
		elif(dirc == 2):   # EAST
			col += 1
		elif(dirc == 4):   # SOUTH
			row += 1
		elif(dirc == 8):	# WEST
			col -= 1
		else:
			print "ERROR: Invalid move direction"
		
		self.rRow = row
		self.rCol = col
		
	def sense(self):
		
		# NORTH
		meas = 0
		if(self.worldMap.isValidSquare(self.rRow-1,self.rCol)):
			meas = meas | 1
		
		# EAST
		if(self.worldMap.isValidSquare(self.rRow,self.rCol+1)):
			meas = meas | 2
			
		# SOUTH
		if(self.worldMap.isValidSquare(self.rRow+1,self.rCol)):
			meas = meas | 4
			
		# WEST
		if(self.worldMap.isValidSquare(self.rRow,self.rCol-1)):
			meas = meas | 8
		
		return meas
		
		
	def run(self):
		self.wg.draw()
		
		self.shadeSquares()
				
		self.wg.drawRobot(self.rRow,self.rCol)
		self.canvas.geometry(self.props["windowDimensions"])
		self.canvas.mainloop()

	def shadeSquares(self):
		probabilities = self.robot.mapProbabilities
		for i in range(0,len(probabilities)):
			for j in range(0,len(probabilities[i])):
				if(self.worldMap.isWall(i,j)==False):
					if(self.robot.mapProbabilities[i][j]>0):      
						# 0 is black, 255 is white
						c = 125 - math.floor(self.robot.mapProbabilities[i][j]*125.0)
						#c = 255 - int(self.robot.mapProbabilities[i][j]*255.0)
						cstr = "#%02x%02x%02x" % (0,c,0)
						self.wg.shadeSquare(i,j,cstr)
					else:
						cstr = "#%02x%02x%02x" % (255,255,255)
						self.wg.shadeSquare(i,j,cstr)
						
	def processEvent(self,event):
		self.robot.move()
		self.robot.sense()
		self.shadeSquares()
		self.wg.drawRobot(self.rRow,self.rCol)
	
def main():
	s = Simulation("WorldMap2.props")
	s.run()
	
if __name__ == '__main__':
	main()
