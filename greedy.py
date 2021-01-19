from random import choice
from valore import Valore
from paziente import Paziente
from soluzione import Soluzione

class Greedy():

	def __init__(self, config):
		self.config = config

	def start(self, istanza, tipoGreedy="LPT" ,casualità=True):
		startAmbulatori = [0,0,0] # Momento libero per ogni ambulatorio

		soluzione = Soluzione(self.config)

		# Creazione ordine di visita in bse al tipo di greedy in uso
		if tipoGreedy == "LPT":
			vettoreIndici = self.LPTGreedy(istanza)
		elif tipoGreedy == "SPT":
			vettoreIndici = self.SPTGreedy(istanza)
		else:
			vettoreIndici = self.FIFOGreedy(istanza)
		
		for indicePaziente in vettoreIndici:
			# Inizializzazione dizionario del nuovo paziente, inserendo anche la voce dei vari jobs. La chiave del dizionario corrisponde all'id del paziente
			soluzione.pazienti[indicePaziente + 1] = paziente = Paziente()
			
			# Uso random per GRASP, scelta casuale tra i due ambulatori migliori
			if casualità:
				idAmbulatorio = self.sceltaGrasp(startAmbulatori)
			else: # GRASP disattivata
				idAmbulatorio = startAmbulatori.index(min(startAmbulatori))
			
			# Ampliamento della voce paziente, inserendo anche l'ambulatorio, l'id paziente, la durata totale degli esami e la posizione nell'ambulatorio
			paziente.ambulatorio = idAmbulatorio
			paziente.id = indicePaziente + 1
			paziente.durataTotale = 0
			paziente.posizione = len(soluzione.ambulatori[idAmbulatorio]) # La prima posizione parte da zero, per essere compatibile con le liste

			# Inserimento dell'intera voce del paziente nella lista degli ambulatori. Viene creato un riferimento tra le due strutture dati primarie
			soluzione.ambulatori[idAmbulatorio].append(paziente)
			
			# Ciclo sugli esami del paziente
			for idEsame in istanza[indicePaziente]:
				paziente.durataTotale += getattr(self.config, "durata" + str(idEsame))
				paziente.ordineEsami.append(idEsame)

				startAmbulatori[idAmbulatorio] = self.aggiungiTask(paziente.esami, indicePaziente + 1, soluzione.esami[idEsame - 1], startAmbulatori[idAmbulatorio], idEsame)
		
		soluzione.calcolaEnergia()
		soluzione.tipoGreedy = tipoGreedy
		soluzione.tipo = "G"
		return soluzione

	'''
	Longest Processing Time. Questa greedy sceglie il paziente che occupa più a lungo gli ambulatori e lo assegna al primo disponibile.
	Ad ogni passo si riduce la lista dei pazienti da poter scegliere.
	'''
	def LPTGreedy(self, istanza):
		durataPazienti = [sum(x) for x in istanza] # Generazione del vettore delle durate
		indiciPazienti = [x for x in range(len(istanza))] # Generazione del vettore degli indici
		
		listaIndici = [] # Soluzione della greedy
		while indiciPazienti: # Fintanto che la lista non è vuota
			indiceCandidato = durataPazienti.index(max(durataPazienti)) # Indice del candidato
			listaIndici.append(indiciPazienti[indiceCandidato]) # Salvo l'indice del paziente nell'istanza da utilizzare successivamente
			
			del durataPazienti[indiceCandidato], indiciPazienti[indiceCandidato] # Rimozione del paziente già scelto
		
		return listaIndici

	'''
	Shortest Processing Time. Questa greedy sceglie il paziente che occupa meno a lungo gli ambulatori e lo assegna al primo disponibile.
	Ad ogni passo si riduce la lista dei pazienti da poter scegliere.
	'''
	def SPTGreedy(self, istanza):
		durataPazienti = [sum(x) for x in istanza] # Generazione del vettore delle durate
		indiciPazienti = [x for x in range(len(istanza))] # Generazione del vettore degli indici
		
		listaIndici = [] # Soluzione della greedy
		while indiciPazienti: # Fintanto che la lista non è vuota
			indiceCandidato = durataPazienti.index(min(durataPazienti)) # Indice del candidato
			listaIndici.append(indiciPazienti[indiceCandidato]) # Salvo l'indice del paziente nell'istanza da utilizzare successivamente
			
			del durataPazienti[indiceCandidato], indiciPazienti[indiceCandidato] # Rimozione del paziente già scelto
		
		return listaIndici
	'''
	First In First Out. Questa greedy sceglie il primo paziente che deve essere servito e lo assegna al primo disponibile.
	La funzione serve per poter aumentare la leggibilità.
	'''
	def FIFOGreedy(self, istanza):
		return [x for x in range(len(istanza))]

	# Funzione che dona la proprietà casuale alla greedy
	def sceltaGrasp(self, ambulatori):
		ambulatoriMigliori = [0, 1] # Inizializzazione lista
		if ambulatori[2] < ambulatori[0]: # Se il terzo ambulatorio è migliore del primo, il primo ambulatorio va scartato si ripete la procedura con lui
			ambulatoriMigliori[0] = 2
			scartato = 0
		elif ambulatori[2] == ambulatori[0]:
			ambulatoriMigliori[0] = choice([0, 2])
			scartato = 2 - ambulatoriMigliori[0]
		else:
			scartato = 2
			
		if ambulatori[scartato] < ambulatori[1]:
			ambulatoriMigliori[1] = scartato
		elif ambulatori[scartato] == ambulatori[1]:
				ambulatoriMigliori[1] = choice([scartato, 1])
		
		return ambulatoriMigliori[choice([0, 1])]
	
	# Funzione che aggiunge il singolo esame di un paziente alla soluzione greedy
	def aggiungiTask(self, esamiPaziente, idPaziente, esami, startAmbulatori, idEsami):
		durata = getattr(self.config, "durata" + str(idEsami)) # Estrazione dinamica della durata del task
		
		if len(esami) > 0: # Se esiste almeno un altro job dello stesso tipo, si verifica se ci sono conflitti
			index = 0
			spazioNonTrovato = True
			while index < len(esami) and spazioNonTrovato: # Ciclo dei job per cercare la posizione in cui inserire quello nuovo
				nuovostartAmbulatori, spazioNonTrovato = self.controlloProssimoJob(startAmbulatori, durata, esami[index][1].valore)  # Aggiunta dell'indice zero per accedere al valore nella lista contenente il singolo valore.
				if spazioNonTrovato:
					startAmbulatori = nuovostartAmbulatori
					index += 1

		esamiPaziente[idEsami] = Valore(startAmbulatori)
		esami.append([idPaziente, esamiPaziente[idEsami]])
		esami.sort(key=lambda x: x[1].valore)

		return startAmbulatori + durata # Ritorno il nuovo startAmbulatori dell'ambulatorio

	# Verifica dei casi possibili: il job osservato è presente (conflitto in atto), futuro (deve ancora incominciare), passato (è già terminato).
	def controlloProssimoJob(self, startAmbulatori, durata, startEsame):
		if startAmbulatori + durata > startEsame and startEsame + durata > startAmbulatori: # Condizione di conflitto
			spazioNonTrovato = True
			return [startEsame + durata, spazioNonTrovato] # startAmbulatori posizionato alla fine del task a destra
		else:
			if startAmbulatori < startEsame: # Sto controllando un job che viene dopo, senza conflitti, quindi posso inserire il nuovo job nel suo startAmbulatori
				spazioNonTrovato = False
				return [startAmbulatori, spazioNonTrovato]
			else: # Il job in analisi è da ignorare in quanto è già terminato all'istante segnato da startAmbulatori
				spazioNonTrovato = True
				return startAmbulatori, spazioNonTrovato