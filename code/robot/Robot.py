from WorldGrid import WorldGrid
import random
import json

class Robot:

	def __init__(self,props,map):
		
		# grab the map information
		self.nRows = props["rows"]
		self.nCols = props["cols"]
		self.map = map
		self.senseCallBack = 0
		self.moveCallBack = 0
		
		self.lastMeasurement = -1
		self.lastMove = -1
		
		# count the number of valid squares
		# in the map
		self.validSquaresCount = 0
		for i in range(0,self.nRows):
			for j in range(0,self.nCols):
				if(self.map.isValidSquare(i,j)):
					self.validSquaresCount += 1
				
		initProb = 1.0 / self.validSquaresCount
		
		# mapProbabilities contains my
		# guess to where I am in the world
		self.mapProbabilities = list()
		for i in range(0,self.nRows):
			row = list()
			for j in range(0,self.nCols):
				if(self.map.isValidSquare(i,j)):
					row.append(initProb)
				else:
					row.append(-1.0)
			self.mapProbabilities.append(row)
			
		# get an encoded version of the map
		# and create a list of squares from that
		encoded = map.encoded_map
		
		self.measures = {}
		for row in range(0,len(encoded)):
			for col in range(0,len(encoded[row])):
				measure = encoded[row][col]
				if measure in self.measures:
					self.measures[measure].append((row,col))
				else:
					self.measures[measure] = [(row,col)]
		
		# finally, initialize a list of probable locations
		# to zero -- we know nothing until we measure
		self.probable_locations = 0
		
	def registerMoveCallBack(self,func):
		self.moveCallBack = func

	def move(self):
	
		# avoid moving opposite of the direction
		# we just moved
		avoid_dir = 2 # set to EAST initially
		if(self.lastMove==1): # moved NORTH last time
			avoid_dir = 4 # don't move SOUTH
		elif(self.lastMove==4): # moved SOUTH last time
			avoid_dir = 1 # don't move NORTH
		elif(self.lastMove==2): # moved EAST last time
			avoid_dir = 8 # don't move WEST
			
		# check for trapped condition
		trapped = False
		if(self.last_measurement == 1 or self.last_measurement == 2 or self.last_measurement == 4 or self.last_measurement == 8):
			trapped = True
	
		# randomly pick a direction to move
		directions = [1,2,4,8]
		found = False
		while found == False:
			dirc = directions[random.randint(0,3)]
			if((dirc & self.last_measurement) and (trapped or dirc != avoid_dir)):
				self.moveCallBack(dirc)
				self.lastMove = dirc
				found = True
		
		# update the probabilities map with the move
		# we make a list of moves and the associated probabilities and 
		# then set the probabilities AFTER making the moves. If we don't,
		# then changing the probability in adjacent squares ruines our
		# probabilities map.
		moved_probabilities = list()
		for i in self.probable_locations:
			nrow = row = i[0]
			ncol = col = i[1]
			if(self.lastMove==1):	# NORTH
				nrow = nrow - 1
			elif(self.lastMove==2):   # EAST
				ncol = ncol + 1
			elif(self.lastMove==4):   # SOUTH
				nrow = nrow + 1
			elif(self.lastMove==8):   # WEST
				ncol = ncol - 1
				
			# move the probabilities
			if(self.map.isValidSquare(nrow,ncol)):
				moved_probabilities.append((nrow,ncol,self.mapProbabilities[row][col]))
		
		# now go through the probable locations and 
		# zero out the probabilities there (we've moved, so we
		# know we can't be at that square any more)
		for i in self.probable_locations:
			self.mapProbabilities[i[0]][i[1]] = 0.0
			
		# finally, loop through the moved-to locations
		# and set their probabilities
		for i in moved_probabilities:
			self.mapProbabilities[i[0]][i[1]] = i[2]
		
	def registerSenseCallBack(self,func):
		self.senseCallBack = func
		
	def sense(self):
		self.last_measurement = self.senseCallBack()
		self.updateProbabilities(self.last_measurement)
		
	def updateProbabilities(self,measurement):
		
		# set my list of probable_locations
		self.probable_locations = self.measures[measurement]
		count = len(self.probable_locations)				
		
		# loop through map probabilities and update based on the 
		# given measurements
		sum = 0.0
		for row in range(0,len(self.mapProbabilities)):
			for col in range(0,len(self.mapProbabilities[row])):
				new_prob = 0.0
				if(self.map.isValidSquare(row,col)):
					prior = self.mapProbabilities[row][col]
					if((row,col) in self.probable_locations):
						new_prob = 1.0/count
					self.mapProbabilities[row][col] = prior * new_prob
					sum += self.mapProbabilities[row][col]
		
		# normalize
		for row in range(0,len(self.mapProbabilities)):
			for col in range(0,len(self.mapProbabilities[row])):
				if(self.map.isValidSquare(row,col)):
					self.mapProbabilities[row][col] = self.mapProbabilities[row][col] / sum
		
	def dumpProbabilities(self):
		str = ""
		for row in range(0,len(self.mapProbabilities)):
			str += "[ "
			for col in range(0,len(self.mapProbabilities[row])):
				str += "%+3.3f " % self.mapProbabilities[row][col]
			str += "]\n"
			
		print str
					
def main():
	props = json.load(open("WorldMap.props"))	
	r = Robot(props)
	
if __name__ == '__main__':
	main()
