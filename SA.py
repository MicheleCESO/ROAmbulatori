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

	raffreddamento = config["Temperatura"] / config["Iterazioni"]
	calore = config["Temperatura"]

	vecchiaEnergia = energia(statoIniziale)

	while calore > 0:
		calore = calore * alpha
		stato = prescelto(statoIniziale)
		# print(stato)
		nuovaEnergia = energia(statoIniziale)
		if nuovaEnergia <= vecchiaEnergia:
			statoIniziale = stato
			vecchiaEnergia = nuovaEnergia
		elif exp(-(nuovaEnergia - vecchiaEnergia)/calore) > uniform(0,1):
			statoIniziale = stato
			vecchiaEnergia = nuovaEnergia

	#	calore -= raffreddamento

		if vecchiaEnergia == 0:
			return statoIniziale
	return [statoIniziale,vecchiaEnergia]

if __name__ == "__main__":
	statoIniziale = [1,2,3,4,5,6,7,8,0]
	shuffle(statoIniziale)
	print("Situazione iniziale: {}\n".format(statoIniziale))
	c = {"Temperatura":2,"Iterazioni":20000}

	res = sa(statoIniziale,c,0.99)
	print(res[0],res[1])
