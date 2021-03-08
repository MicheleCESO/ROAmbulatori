from random import randint, uniform, choice	# Per la casualità
from copy import deepcopy

class Istanza():
	def __init__(self, config):
		self.config = config
	
	'''
	Funzione per generare un'istanza. Prima crea un numero casuale di pazienti partendo dalle impostazioni, poi per ogni paziente crea da 1 a 5 esami, scegliendo tra quelli possibili.
	Gli esami già utilizzati non vengono presi in considerazione per le estrazioni future dello stesso paziente.
	'''
	def start(self):
		nPazienti = randint(self.config.minPazienti, self.config.maxPazienti)

		risultato = []
		
		dictProbabilitàNEsami = {1: self.config.p1Esami, 2: self.config.p2Esami, 3: self.config.p3Esami, 4: self.config.p4Esami, 5: self.config.p5Esami}
		soglieProbNumeroEsami = self.creaSoglie(dictProbabilitàNEsami)
		maxRandomNEsami = sum(dictProbabilitàNEsami.values())

		dictProbabilitàTipoEsami = {1: self.config.pEsame1, 2: self.config.pEsame2, 3: self.config.pEsame3, 4: self.config.pEsame4, 5: self.config.pEsame5}

		for _ in range(nPazienti):
			# Quanti esami?
			numeroEsami = self.trovaSoglia(soglieProbNumeroEsami, uniform(0, maxRandomNEsami))

			# Quali esami?
			i = 0
			dictSoglie = deepcopy(dictProbabilitàTipoEsami) # Copia delle probabilità degli esami per preservazione delle informazioni
			esami = []
			while i < numeroEsami:
				
				# Calcolo soglie
				soglieProbTipoEsami = self.creaSoglie(dictSoglie)
				maxRandomTipoEsami = sum(dictSoglie.values())
				
				listaEsamiCerti = self.trovaEsamiCerti(dictSoglie)
				
				if len(listaEsamiCerti) > 0:
					tipoEsame = choice(listaEsamiCerti)
				else:
					tipoEsame = self.trovaSoglia(soglieProbTipoEsami, uniform(0, maxRandomTipoEsami)) # Calcolo tipo di esame in base alla soglia

				esami.append(tipoEsame) # Salvataggio esame richiesto
				i += 1

				del dictSoglie[tipoEsame] # Cancello elemento per non riestrarlo più

			risultato.append(esami) # Salvataggio del paziente

		return risultato

	'''
	Funzione per rilevare esami sicuramente richiesti dall'istanza.
	'''
	def trovaEsamiCerti(self, dictSoglie):
		listaEsami = []
		for chiave, valore in dictSoglie.items():
			if valore >= 100:
				listaEsami.append(chiave)
		return listaEsami
	'''	
	Metodo per creare le soglie di probabilità per poter decidere quali e quanti esami associare al singolo paziente
	'''
	def creaSoglie(self, dictProbabilità):
		offset = 0
		soglie = {}
		for chiave, valore in dictProbabilità.items():
			if valore != 0:
				soglie[chiave] = offset + valore # Inserisco il limite massimo della probabilità
				offset += valore # Ricalcolo dell'offset
			else:
				soglie[chiave] = -1 # Soglia negativa, non verrà utilizzata successivamente
		return soglie
	
	'''
	Metodo per trovare la soglia giusta dato un valore casuale da 0 a 100
	'''
	def trovaSoglia(self, soglie, valore):
		for chiave in soglie.keys():
			if soglie[chiave] >= valore:
				return chiave
		
if __name__ == "__main__":
	from config import Config
	config = Config()
	classe = Istanza(config)
	ris = classe.start()
	print(ris)