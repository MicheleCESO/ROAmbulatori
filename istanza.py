from itertools import permutations	# Per gestire le combinazioni di task
from random import randint, choice, shuffle, uniform	# Per la casualità

class Istanza():
	def __init__(self, config):
		self.config = config
	
	'''
	Funzione per generare un'istanza. Prima crea un numero casuale di pazienti partendo dalle impostazioni, poi per ogni paziente crea da 1 a 5 esami, indicando sempre casualmente la tipologia
	'''
	def start(self):
		nPazienti = randint(self.config.minPazienti, self.config.maxPazienti)

		risultato = []
		
		listaProbabilitàNEsami = [self.config.p1Esami, self.config.p2Esami, self.config.p3Esami, self.config.p4Esami, self.config.p5Esami]
		soglieProbNumeroEsami = self.creaSoglie(listaProbabilitàNEsami)
		maxRandomNEsami = sum(listaProbabilitàNEsami)
		
		listaProbabilitàPresenzaEsami = [self.config.pEsame1, self.config.pEsame2, self.config.pEsame3, self.config.pEsame4, self.config.pEsame5]
		soglieProbTipoEsami = self.creaSoglie(listaProbabilitàPresenzaEsami)
		maxRandomTipoEsami = sum(listaProbabilitàPresenzaEsami)

		for _ in range(nPazienti):
			# Quanti esami?
			numeroEsami = self.trovaSoglia(soglieProbNumeroEsami, round(uniform(0, maxRandomNEsami), 2))
			
			esami = []
			# Quali esami?
			i = 0
			while i < numeroEsami:
				tipoEsame = self.trovaSoglia(soglieProbTipoEsami, round(uniform(0, maxRandomTipoEsami), 2))
				if tipoEsame not in esami:
					esami.append(tipoEsame)
					i += 1
			
			risultato.append(esami)

		return risultato
	
	'''	
	Metodo per creare le soglie di probabilità per poter decidere quali e quanti esami associare al singolo paziente
	'''
	def creaSoglie(self, lista):
		offset = 0
		res = []
		for el in lista:
			if el != 0:
				res.append(offset + el) # Inserisco il limite massimo della probabilità
				offset += el # Ricalcolo dell'offset
			else:
				res.append(-1) # Soglia negativa, non verrà utilizzata successivamente
		return res
	
	'''
	Metodo per trovare la soglia giusta dato un valore casuale da 0 a 100
	'''
	def trovaSoglia(self, soglie, valore):
		i = 0
		while soglie[i] < valore:
			i += 1
		return i + 1 # Indice trasformato in tipo di esame