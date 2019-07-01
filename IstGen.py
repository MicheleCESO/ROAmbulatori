from random import randint

def genIstanza():
	minP = 1
	maxP = 10

	nPazienti = randint(minP,maxP)

	minT = 1
	maxT = 5

	risultato = []

	for i in range(nPazienti):
		risultato.append([])

		# Quanti esami?
		nT = randint(minT,maxT)

		# Quali esami?
		for j in range(nT):
			esame = randint(minT,maxT)
			if esame not in risultato[i]:
				risultato[i].append(esame)

	return risultato