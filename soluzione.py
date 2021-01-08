class Soluzione():
	def __init__(self, config):
		self.config = config
		self.pazienti = {} 							# Struttura contenente informazioni su tutti i pazienti
		self.esami = [[] for _ in range(5)]			# Ogni sottolista contiene un elenco di start di un certo tipo di esame assegnati 
													# agli ambulatori
		self.ambulatori = [[] for _ in range(3)]	# Liste contenenti i pazienti in ordine cronologico per ogni ambulatorio

		self.energia = None							# Bontà della soluzione
		self.efficienza = None						# Quanto è efficiente la soluzione
		self.makeSpan = None						# Il punto in cui l'ultimo ambulatorio smette di lavorare
	'''
	Funzione per calcolare l'energia di uno stato.
	Il calcolo si basa sulla quantità di spazio non utilizzato che va dall'istante zero, all'istante dell'ultimo ambulatorio che finisce gli esami, ciò definisce una soglia di analisi.
	Non importa se un ambulatorio termina prima dell'istante definito dalla soglia, tutta quest'area viene considerata negativa, in quanto l'ambulatorio potrebbe eseguire degli esami per alleggerire l'ambulatorio che sta ancora lavorando.
	'''
	def calcolaEnergia(self, soluzione):
		ultimoJob = [max(soluzione.ambulatori[i][-1].esami.items(), key=lambda k: k[1].valore) for i in range(3) if len(soluzione.ambulatori[i]) > 0] # Crea una lista contenente l'ultimo job di ogni ambulatorio
		tipoJob, sogliaStart = max(ultimoJob, key=lambda k: k[1].valore + getattr(self.config, "durata" + str(k[0]))) # Restituisce due elementi: il tipo di job ed il suo start
		makeSpan = sogliaStart.valore + getattr(self.config, "durata" + str(tipoJob))

		Etot = 0

		efficienza = []

		for i in range(3): # Per ogni ambulatorio
			energiaFinale = makeSpan
			for paziente in soluzione.ambulatori[i]: # Per ogni paziente
				for job in paziente.ordineEsami: # Per ogni job
					energiaFinale -= getattr(self.config, "durata" + str(job))
			efficienza.append((makeSpan - energiaFinale) / makeSpan) # Calcolo dell'efficienza di un ambulatorio
			Etot += energiaFinale
		
		soluzione.energia = Etot
		soluzione.efficienza = efficienza
		soluzione.makeSpan = makeSpan

	'''
	Questa funzione controlla se ci sono conflitti tra i vari pazienti.
	Inizialmente si cerca il punto corretto da cui controllare eventuali conflitti, in quanto è possibile sia avvenuta una compattazione prima della soglia fissata.
	Si cercano i candidati al controllo basandosi sugli indici dei pazienti analizzati, controllando l'attributo "volatile" è possibile capire se considerare i conflitti ottenuti o no.
	Il ciclo si ripete finché tutti gliambulatori hanno esaurito i pazienti (candidati).
	'''
	def controlloConflitto(self, indici):
		indAmbulatori = []
		for i in range(3): # Creazione dinamica della lista degli ambulatori in cui controllare i conflitti
			if indici[i] != len(self.ambulatori[i]):
				indAmbulatori.append(i)

		spostamento = [0, 0, 0] # Spostamento dei job nel caso ci siano conflitti
		
		candidati = {i: min(self.ambulatori[i][indici[i]].esami.values(), key=lambda x: x.valore).valore for i in indAmbulatori} # Crea un dizionario contenente gli start minimi dei pazienti interessati (volatili)
		while len(candidati) > 0: # Fintanto che ci sono ambulatori con pazienti da controllare
			minAmbulatorio = min(candidati, key=candidati.get) # Indice dell'ambulatorio del candidato che parte prima degli altri
			spostamento[minAmbulatorio] = self.risolviConflitto(self.ambulatori[minAmbulatorio][indici[minAmbulatorio]], spostamento[minAmbulatorio])

			if indici[minAmbulatorio] == len(self.ambulatori[minAmbulatorio]) - 1: # Significa che è stato osservato l'ultimo paziente dell'ambulatorio
				indAmbulatori.remove(minAmbulatorio) # Rimozione dell'ambulatorio dalla lista degli ambulatori da controllare
			else:
				indici[minAmbulatorio] += 1
			candidati = {i: min(self.ambulatori[i][indici[i]].esami.values(), key=lambda x: x.valore).valore for i in indAmbulatori}
	
	'''
	Risolve i conflitti del paziente in uso.
	Viene esaminato un esame per volta. Subito si sposta l'esame in corso in base agli spostamenti fatti per gli esami precedenti (anche quelli degli altri pazienti) inerenti al medesimo ambulatorio.
	Viene mantenuto l'ordine cronologico degli esami dello stesso tipo e si verificano i vicini di sinistra e destra. Se si trova posto libero, si inserisce l'esame del paziente e si passa al prossimo esame.
	'''
	def risolviConflitto(self, paziente, spostamento):
		for tipoEsame in paziente.ordineEsami:
			startEsame = paziente.esami[tipoEsame]
			startEsame.valore += spostamento # Spostamento è la somma degli spostamenti fatti degli esami precedenti del ciclo for

			self.esami[tipoEsame - 1].sort(key=lambda x: x[1].valore) # Il sorting utilizzato ha la caratteristica di essere stabile
			index = [x[0] for x in self.esami[tipoEsame - 1]].index(paziente.id) # Calcolo posizione paziente nella lista
	
			# Controllo conflitto elemento a sinistra
			if index > 0:
				j = 1
				while index - j >= 0 and self.pazienti[self.esami[tipoEsame - 1][index-j][0]].volatile: # Si cerca il primo esame volatile che si trova a sinistra
					j += 1
				if index - j >= 0 and self.esami[tipoEsame - 1][index-j][1].valore + getattr(self.config, "durata" + str(tipoEsame)) > startEsame.valore: # Se la fine dell'esame precedente supera l'inizio dell'esame attuale
					delta = self.esami[tipoEsame - 1][index - j][1].valore + getattr(self.config, "durata" + str(tipoEsame)) - startEsame.valore # Calcolo spostamento necessario (delta) dell'esame in caso di conflitto
					startEsame.valore += delta
					spostamento += delta
					self.esami[tipoEsame - 1].sort(key=lambda x: x[1].valore) # Il sorting utilizzato ha la caratteristica di essere stabile
					index = [x[0] for x in self.esami[tipoEsame - 1]].index(paziente.id) # Aggiornamento dell'indice
			
			# Controllo conflitto elemento a destra
			if index < len(self.esami[tipoEsame - 1]) - 1:	
				j = 1
				while index + j < len(self.esami[tipoEsame - 1]) and startEsame.valore + getattr(self.config, "durata" + str(tipoEsame)) > self.esami[tipoEsame - 1][index + j][1].valore: # Se l'esame termina dopo l'inizio dell'esame successivo, si ha conflitto
					if not(self.pazienti[self.esami[tipoEsame - 1][index + j][0]].volatile) : # Se l'esame che crea confitto non è volatile, il conflitto va risolto
						delta = self.esami[tipoEsame - 1][index + j][1].valore + getattr(self.config, "durata" + str(tipoEsame)) - startEsame.valore # Spostamento in avanti in caso di conflitto
						startEsame.valore += delta
						spostamento += delta
						self.esami[tipoEsame - 1].sort(key=lambda fun: fun[1].valore) # Il sorting utilizzato ha la caratteristica di essere stabile
					j += 1
		paziente.volatile = False # Il paziente è permanentemente fissato
		
		return spostamento

	'''
	Funzione generale che gestisce la compressione degli ambulatori.
	'''
	def compattaAmbulatori(self, startMin):
		# Compattamento degli ambulatori nell'area che inizia con lo start minimo dei pazienti scambiati
		indiciPazienti = [0, 0, 0] # Indici dei pazienti da cui partire per verificare i conflitti
		for i in range(3):
			indiciPazienti[i] = self.compattaAmbulatorio(self.ambulatori[i], startMin)

		return indiciPazienti

	'''
	Per l'ambulatorio corrente viene eseguita una compressione dei pazienti che terminano dopo lo start minimo in cui avviene un cambiamento.
	Un ciclo while ha il compito di determinare il primo paziente che ricade nell'area di compressione (soglia in base allo start minimo dei pazienti spostati), allo stesso tempo tenendo in memoria la fine del paziente precedente.
	Terminato il ciclo, viene avviata la procedura di compattazione per ogni paziente presente dopo l'indice trovato.
	'''
	def compattaAmbulatorio(self, listaPazienti, startMin):
		index = 0	# Indice nella lista dei pazienti
		if len(listaPazienti) > 0:
			posizioneInserimento = None # Offset di inserimento in caso di compattazione paziente. Coincide con la fine del paziente precedente
			
			# Il ciclo ha il compito di trovare il primo paziente che si trova nell'area di compressione
			chiaveMaxStart = max(listaPazienti[index].esami, key=lambda x: listaPazienti[index].esami[x].valore) # Chiave del job che inizia più tardi
			while index < len(listaPazienti) and listaPazienti[index].esami[chiaveMaxStart].valore + getattr(self.config, "durata" + str(chiaveMaxStart)) <= startMin: # Se ci sono pazienti e la fine edl job massimo è più piccola della soglia, il paziente va saltato
				listaPazienti[index].volatile = False # Il paziente viene considerato fisso
				posizioneInserimento = listaPazienti[index].esami[chiaveMaxStart].valore + getattr(self.config, "durata" + str(chiaveMaxStart))
				index += 1
				if index < len(listaPazienti):
					chiaveMaxStart = max(listaPazienti[index].esami, key=lambda x: listaPazienti[index].esami[x].valore)

		# Ora sono presenti solo pazienti che sono di tipo volatile, ovvero soggetti ala modifica dei loro esami
		# Da notare che se tutti i pazienti non sono da compattare, la funzione sottostante non viene chiamata
		for paziente in listaPazienti[index:]:
			posizioneInserimento = self.compattaPaziente(paziente, startMin, posizioneInserimento) # Compatta il paziente e ritorna il nuovo offset da usare di nuovo

		return index

	'''
	Funzione per compattare il singolo paziente.
	Inizialmente se non ci sono pazienti antecedenti alla compattazione l'offset iniziale passa da None a 0.
	Il paziente viene evidenziato come volatile, ovvero non fissato definitivamente nella posizione che occupa, poi si verifica ogni esame che deve fare:
	se l'esame inizia prima della soglia fissata, non gli viene alterata la posizione, perché si suppone che i vincoli che l'hanno posizionato sono ancora attivi, in quanto appartenenti ad un'area non alterata rispetto la soluzione precedente.
	Se invece l'esame inizia dopo la soglia, allora va spostato a sinistra il più possibile, al massimo va posizionato alla fine del paziente precedente oppure dopo il job analizato prima.
	'''
	def compattaPaziente(self, paziente, sogliaStart, posizioneInserimento):
		if posizioneInserimento == None: # Se non esistono pazienti prima del compattamento, l'inserimento parte dall'inizio
			posizioneInserimento = 0
		paziente.volatile = True
		for tipoEsame in paziente.ordineEsami:
			startEsame = paziente.esami[tipoEsame]

			if startEsame.valore < sogliaStart:
				posizioneInserimento = startEsame.valore + getattr(self.config, "durata" + str(tipoEsame)) # Calcolo fine del job attuale
			else:
				startEsame.valore = posizioneInserimento
				posizioneInserimento += getattr(self.config, "durata" + str(tipoEsame))
		return posizioneInserimento

	'''
	Funzione che genera una matrice indicante la sequenza cronologica di tutti i pazienti, indicante tutti gli id. 
	'''
	def generaMatricePosizione(self, ambulatori):
		matrice = []
		for i in range(3): # Per ogni ambulatorio
			matrice.append([])
			for paziente in ambulatori[i]:
				matrice[i].append(paziente.id)
		return matrice