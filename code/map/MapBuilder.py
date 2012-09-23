import json

class WorldMap:

	def __init__(self,propsfile):
	
		props = json.load(open(propsfile))
		self.nRows = props['rows']
		self.nCols = props['cols']
		self.map = props['map']
		
		self.encoded_map = self.encodeMap()
		
	def __str__(self):
		string = "Map:\n"
		for i in range(0,len(self.map)):
			string +=  str(self.map[i]) + "\n"
		string += "Encoded Map:\n"
		for i in range(0,len(self.encoded_map)):
			string += str(self.encoded_map[i]) + "\n"
		return string
		
	def isOnMap(self,row,col):
		return ((col>=0 and col<self.nCols) and (row>=0 and row<self.nRows))
		
	def isWall(self,row,col):
		return self.isOnMap(row,col) and (self.map[row][col]==1)
		
	def isValidSquare(self,row,col):
		return self.isOnMap(row,col) and self.isWall(row,col) == False
				
	# encode the map with the possible directions
	# from each square
	def encodeMap(self):
		encode = list()
		for row in range(0,self.nRows):
			r = list()
			for col in range(0,self.nCols):
				code = 0 # initialize to no directions

				if(self.isWall(row,col)==False):
						# check north
						if(self.isValidSquare(row-1,col)):
						   code = code | 1
						   
						# check east
						if(self.isValidSquare(row,col+1)):
						   code = code | 2
						   
						# check south
						if(self.isValidSquare(row+1,col)):
						   code = code | 4
						   
						# check west
						if(self.isValidSquare(row,col-1)):
						   code = code | 8
						   
						r.append(code)
				else:
						r.append(-1)
			encode.append(r)
		
		return encode
		
def main():
	wm = WorldMap("WorldMap.props")
	print wm
	
	# test isValidSquare method
	print "Test isValidSquare:"
	for i in range(-1,wm.nRows+1):
		string = "[ "
		for j in range(-1,wm.nCols+1):
			if(wm.isValidSquare(i,j)):
				string += "T "
			else:
				string += "F "
		print string,"]"
	
if __name__ == '__main__':
	main()
