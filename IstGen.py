from itertools import permutations	# Per gestire le combinazioni di task
from random import randint, choice	# Per la casualità

# Funzione per generare un'istanza.
# Il numero di job che può possedere un paziente, oscilla da 1 a 5.
def genIstanza(conf):
	nPazienti = randint(conf.minPazienti, conf.maxPazienti)

	listaJobs = [i for i in range(1, 6)] # Da 1 a 5 jobs

	risultato = []

	for i in range(nPazienti):
		# Quanti esami?
		nT = randint(1, 5) # Da 1 a 5 jobs

		# Quali esami?
		esami = choice(list(permutations(listaJobs, nT)))	# Prima permuto la lista degli esami con il numero richiesto, poi prendo un elemento a caso
		risultato.append(list(esami))
		print(esami)

	return risultato