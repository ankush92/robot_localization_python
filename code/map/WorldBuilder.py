from SimpleGrid import SimpleGrid
from Tkinter import Tk
from WorldMap import WorldMap
import random
import json
import math

# We need a different grid object for this -- this grid will be clickable
# and provide a callback to notify clients when a grid cell has been clicked
# This will allow us to color a grid cell when clicked
#
# We will also need to keep state of each grid cell (clicked, not clicked, etc.),
# so that if the users clicks a cell twice, the color of the cell can toggle
#
# We need to work on the initialization of the application. This really requires
# the ability to resize the grid when the user resizes the window
#
# We need a menubar with a file menu, etc.
#
# Application will allow the user to save, load and edit a worldmap file
#

class WorldBuilder:

	def __init__(self):
		self.canvas = Tk()
		
		#self.props = json.load(open(propsfile))
		#self.worldMap = WorldMap(propsfile)
		
		#self.wg = WorldGrid(self.canvas,self.props,self.worldMap)
		#self.wg.registerCallBack(self.processEvent)
		
		self.props = { "rows":10, "cols":10, "width":500, "height":500, "windowDimensions":"500x500" }
		self.sg = SimpleGrid(self.canvas,self.props)
		
	def run(self):
		self.sg.draw()
		self.canvas.geometry(self.props["windowDimensions"])
		self.canvas.mainloop()

def main():
	s = WorldBuilder()
	s.run()
	
if __name__ == '__main__':
	main()
