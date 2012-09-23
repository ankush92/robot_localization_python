import sys

sys.path.append("./simulation")

from Simulation import Simulation

def main():
	s = Simulation("../properties/WorldMap2.props")
	s.run()
	
if __name__ == '__main__':
	main()
