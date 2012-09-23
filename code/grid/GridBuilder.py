from WorldGrid import WorldGrid
from Tkinter import Tk
from WorldMap import WorldMap
import random
import json
import math


class WorldBuilder:

	def __init__(self,propsfile):
		self.canvas = Tk()
		
		self.props = json.load(open(propsfile))
		#self.worldMap = WorldMap(propsfile)
		
		self.wg = WorldGrid(self.canvas,self.props,self.worldMap)
		self.wg.registerCallBack(self.processEvent)
