from math import exp		# Per l'esponenziale e
from random import uniform	# Per generare numeri pseudocasuali (0,1)
from random import shuffle,randint
# Funzione per generare un vicino da confrontare con lo stato attuale
def prescelto(statoIniziale):
	index = statoIniziale.index(0)
	mosse = {
				0:[1,3],
				1:[0,2,4],
				2:[1,5],
				3:[0,4,6],
				4:[1,3,5,7],
				5:[2,4,8],
				6:[3,7],
				7:[4,6,8],
				8:[5,7]
	}

	indexToSwap = randint(0,len(mosse[index])-1)
	statoIniziale[index] = statoIniziale[mosse[index][indexToSwap]]
	statoIniziale[mosse[index][indexToSwap]] = 0
	return statoIniziale

# Funzione per calcolare l'energia di uno stato
def energia(stato):
	i = 0
	energia = 0
	for element in stato:
		if element != i+1:
			energia += 1
		i += 1
	if stato[-1] == 0:
		energia -= 1
	return energia

# Simulated Annealing
def sa(statoIniziale,config,alpha):

	raffr = config["Temperatura"] / config["Iterazioni"]
	calore = config["Temperatura"]

	iter = 0

	vecchiaEnergia = energia(statoIniziale)

	while calore > 0 and iter < config["Iterazioni"]:
		calore = calore * alpha
		stato = prescelto(statoIniziale)

		nuovaEnergia = energia(statoIniziale)
		if nuovaEnergia <= vecchiaEnergia:
			statoIniziale = stato
			vecchiaEnergia = nuovaEnergia
		elif exp(-(nuovaEnergia - vecchiaEnergia)/calore) > uniform(0,1):
			statoIniziale = stato
			vecchiaEnergia = nuovaEnergia

		if vecchiaEnergia == 0:
			return [statoIniziale, True]
		iter += 1
	return [statoIniziale, False]

if __name__ == "__main__":
	statoIniziale = [1,2,3,4,5,6,7,8,0]
	shuffle(statoIniziale)
	print("Situazione iniziale: {}\n".format(statoIniziale))
	c = {"Temperatura":2,"Iterazioni":200000}

	res = sa(statoIniziale,c,0.99)
	while not res[1]:
		print(res[0],"Rifaccio....")
		res = sa(res[0],c,0.99)
	print(res)
