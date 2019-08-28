from itertools import permutations	# Per gestire le combinazioni di task
from random import randint, choice	# Per la casualità

# Funzione per generare un'istanza
def genIstanza(conf):
	nPazienti = randint(conf["MinPazienti"],conf["MaxPazienti"])

	listaJobs = [i for i in range(conf["MinTasks"],conf["MaxTasks"]+1)]

	risultato = []

	for i in range(nPazienti):
		# Quanti esami?
		nT = randint(conf["MinTasks"],conf["MaxTasks"])

		# Quali esami?
		esami = choice(list(permutations(listaJobs,nT)))	# Prima permuto la lista degli esami con il numero richiesto, poi prendo un elemento a caso
		risultato.append(list(esami))
		print(esami)

	return risultato