from math import exp		# Per l'esponenziale e
from random import shuffle,randint,choice, uniform
from copy import deepcopy

class SimulatedAnnealing():
	def __init__(self, config):
		self.config = config

	'''
	Funzione per generare un vicino da confrontare con lo stato attuale (eseguire una mossa"):
	Si effettua la duplicazione dello stato attuale in modo da poter annullare la mossa successivamente, ripristinando lo stato vecchio.
	Si sceglie se scambiare due pazienti o spostarne uno solo in coda ad un ambulatorio casuale.
	A prescindere dal tipo di mossa scelta, viene calcolata la soglia minima che comporta una compattazione nei 3 ambulatori (dalla soglia fino al punto più lontano).
	Prima di completare il nuovo stato, bisogna sottolineare che possono essere presenti due tipi di conflitti, nella nuova soluzione:
	-	Conflitti orizzontali: si tratta di sovrapposizioni di esami posti negli stessi ambulatori. Per eliminarli si può compattare i pazienti da una certa soglia, quella oltre la quale si ha delle variazioni. Prima della soglia non è cambiato nulla, quindi
		si presuppone che tutti i vincoli siano ancora attivi, perciò non serve compattare nulla.
	-	Conflitti verticali: si tratta di esami dello stesso tipo che sono attivi nello stesso tempo, non rispettando il vincolo indicante che in qualsiasi momento, non può essere eseguito più di un esame alla volta del medesimo tipo
		(infatti c'è un dottore per ogni tipo di eame). Per risolvere questi conflitti, si parte dal presupposto che dopo la compattazione si creano due categorie di pazienti, quelli volatili e quelli non volatili. I non volatili sono i pazienti che non sono stati
		compattati, perciò vengono trattati come se fossero già posizionati correttamente. Quelli volatili invece sono i pazienti soggetti a compattazione, perciò viene indicato che non hanno ancora una posizione definitiva. La risoluzione prevede quindi di controllare
		solo i pazienti volatili, in modo da trovargli una posizione finale, rendendoli perciò non volatili. Il conflitto viene identificato solo in caso si trovino pazienti non volatili.		
	Si compattano tutti gli ambulatori, tornando l'indice del primo paziente che è stato compresso.
	Infine viene effettuato un controllo per risolvere tutti i conflitti (verticali) dei pazienti.
	'''
	def mossa(self, soluzioneCorrente):
		soluzioneNuova = deepcopy(soluzioneCorrente) # Copia dello stato attuale
		
		# Scelta della prossima mossa, il ramo if esegue uno scambio tra pazienti, il ramo else sposta un singolo paziente casuale in coda ad un ambulatorio casuale
		if uniform(0, 1) <= self.config.probabilitàScambio:
			paziente1, paziente2 = self.swapPazienti(soluzioneNuova.pazienti, soluzioneNuova.ambulatori)
			startMin = min(list(paziente1.esami.values()) + list(paziente2.esami.values()), key=lambda x: x.valore).valore # L'esame che inizia prima dei due pazienti
		else:
			paziente = self.spostamentoPaziente(soluzioneNuova.ambulatori)
			startMin = min(paziente.esami.values(), key=lambda x: x.valore).valore # L'esame che inizia prima
		
		indiciPazienti = soluzioneNuova.compattaAmbulatori(startMin)
		
		soluzioneNuova.controlloConflitto(indiciPazienti)

		return soluzioneNuova

	'''
	Funzione per scambiare le posizioni di due pazienti casuali.
	Inizialmente si determinano quali pazienti utilizzare per lo scambio (si considerano le strutture dati complete dei pazienti, non solo gli indici)
	Vengono poi estratte le posizioni dei due pazienti dai rispettivi ambulatori, in modo che successivamente si possa alterare la loro ubicazione nella struttura dati degli ambulatori.
	Infine si scambia il dato che indica dove si trovano i pazienti.
	'''
	def swapPazienti(self, solPazienti, statoAmbulatori):
		# Estrazione casuale pazienti
		paziente1 = choice(list(solPazienti.values()))
		paziente2 = choice(list(solPazienti.values()))
		while paziente2 == paziente1:
			paziente2 = choice(list(solPazienti.values()))

		# Estrapolazione posizione pazienti nella struttura ambulatori
		index1 = statoAmbulatori[paziente1.ambulatorio].index(paziente1)
		index2 = statoAmbulatori[paziente2.ambulatorio].index(paziente2) 
		
		# Scambio strutture dati
		temp = statoAmbulatori[paziente1.ambulatorio][index1]
		statoAmbulatori[paziente1.ambulatorio][index1] = statoAmbulatori[paziente2.ambulatorio][index2]
		statoAmbulatori[paziente2.ambulatorio][index2] = temp

		# Scambio informazione ambulatorio
		tempAmbulatorio = paziente1.ambulatorio
		paziente1.ambulatorio = paziente2.ambulatorio
		paziente2.ambulatorio = tempAmbulatorio

		# Scambio informazione posizione
		tempPosizione = paziente1.posizione
		paziente1.posizione = paziente2.posizione
		paziente2.posizione = tempPosizione

		# Modifica ordine esami
		shuffle(paziente1.ordineEsami)
		shuffle(paziente2.ordineEsami)
		
		return paziente1, paziente2
	
	'''
	Funzione per spostare un paziente casuale in coda ad un ambulatorio casuale.
	'''
	def spostamentoPaziente(self, statoAmbulatori):
		# Scelta del paziente da spostare
		ambulatorioCasuale = randint(0, len(statoAmbulatori) - 1)
		while len(statoAmbulatori[ambulatorioCasuale]) == 0: # Gli ambulatori vuoti non vengono scelti
			ambulatorioCasuale = randint(0, len(statoAmbulatori) - 1)

		pazienteCasuale = randint(0, len(statoAmbulatori[ambulatorioCasuale]) - 1)
		candidato = statoAmbulatori[ambulatorioCasuale].pop(pazienteCasuale)
		
		# Aggiorno la posizione di ogni paziente dopo quello estratto
		for paziente in statoAmbulatori[ambulatorioCasuale][candidato.posizione:]:
			paziente.posizione -= 1

		# Spostamento del paziente
		ambulatorioCasuale = randint(0, len(statoAmbulatori) - 1)
		statoAmbulatori[ambulatorioCasuale].append(candidato)
		candidato.ambulatorio = ambulatorioCasuale
		candidato.posizione = len(statoAmbulatori[ambulatorioCasuale]) - 1

		#Modifica ordine esami
		shuffle(candidato.ordineEsami)
		
		return candidato

	'''
	Funzione principale del Simulated Annealing.
	L'algoritmo crea una nuova soluzione applicando una "mossa" (scambio di pazienti o spostamento di un singolo paziente in coda ad un amvbulatorio) alla soluzione attuale, successivamente compara l'energia delle due soluzioni:
	-	Se la nuova energia è minore, significa che nella nuova soluzione sono presenti meno zone "idle", indicando una miglioria nella soluzione attuale.
	-	Se la nuova energia è maggiore, significa che la soluzione appena trovata è peggiore della precedente, quindi l'algoritmo sceglie se mantenerla ugualmente o scartarla in maniera definitiva. Per farlo, utilizza una formula per definire la probabilità
		di mantenerla ugualmente (exp(- delta / temperatura)).
	Queste scelte si ripetono ad ogni iterazione, fino al raggiungimento della soglia impostata dall'utente. A questo punto viene ritornata la soluzione finale, quella che alla fine risulta con l'energia minore.
	'''
	def start(self, soluzioneCorrente):
		print("\nIn esecuzione...")
	
		itera = 0;
		calore = self.config.temperatura
		
		soluzioneCorrente.calcolaEnergia()
		while itera < self.config.iterazioni:
			calore = calore * self.config.tassoRaffreddamento
			soluzioneNuova = self.mossa(soluzioneCorrente)
			soluzioneNuova.calcolaEnergia()
			
			# Se la soluzione nuova è migliore o nonostante sia peggiore, viene deciso di mantenerla, sostituendo la vecchia energia e soluzione
			if soluzioneNuova.energia <= soluzioneCorrente.energia or exp(-(soluzioneNuova.energia - soluzioneCorrente.energia)/calore) > uniform(0, 1):
				soluzioneCorrente = soluzioneNuova
			itera += 1
		soluzioneCorrente.tipo = "SA"
		return soluzioneCorrente