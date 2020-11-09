from euristica import *

def main():
	ist = [[5], [5], [2, 4, 5, 1], [3], [5, 2], [4], [5, 2], [2, 3, 1, 5], [2], [1], [5, 3, 1], [5], [1, 4], [4], [1, 2, 3]]
	durata = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
	pazienti1, jobs, ambulatori = euri(ist, durata, True)
	
	pazienti2, jobs, ambulatori = euri(ist, durata, True)
	print(pazienti1)
	print(pazienti2)

if __name__ == "__main__":
	main()