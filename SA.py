from math import exp		# Per l'esponenziale e
from random import uniform	# Per generare numeri pseudocasuali
from random import shuffle,randint,choice
from disegno import disegna
from copy import deepcopy

class SA():
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
	def mossa(self, statoCorrente):
		statoNuovo = deepcopy(statoCorrente) # Copia dello stato attuale
		
		solPazienti = statoNuovo[0]
		statoLavori = statoNuovo[1]
		statoAmbulatori = statoNuovo[2]
		
		# Scelta della prossima mossa, il ramo if esegue uno scambio tra pazienti, il ramo else sposta un singolo paziente casuale in coda ad un ambulatorio casuale
		if uniform(0, 1) <= self.config.probabilitàScambio:
			paziente1, paziente2 = self.swapPazienti(solPazienti, statoAmbulatori)
			startMin = min(list(paziente1["jobs"].values()) + list(paziente2["jobs"].values()), key=lambda x: x.valore).valore # L'esame che inizia prima dei due pazienti
		else:
			paziente = self.spostamentoPaziente(statoAmbulatori)
			startMin = min(paziente["jobs"].values(), key=lambda x: x.valore.valore) # L'esame che inizia prima
		
		# Compattamento degli ambulatori nell'area che inizia con lo start minimo dei pazienti scambiati
		indiciPazienti = [0, 0, 0] # Indici dei pazienti da cui partire per verificare i conflitti
		for i in range(3):
			indiciPazienti[i] = self.compattaAmbulatorio(statoAmbulatori[i], startMin)
		
		self.controlloConflitto(solPazienti, indiciPazienti, statoLavori, statoAmbulatori)

		return statoNuovo

	'''
	Questa funzione controlla se ci sono conflitti tra i vari pazienti.
	Inizialmente si cerca il punto corretto da cui controllare eventuali conflitti, in quanto è possibile sia avvenuta una compattazione prima della soglia fissata.
	Si cercano i candidati al controllo basandosi sugli indici dei pazienti analizzati, controllando l'attributo "volatile" è possibile capire se considerare i conflitti ottenuti o no.
	Il ciclo si ripete finché tutti gliambulatori hanno esaurito i pazienti (candidati).
	'''
	def controlloConflitto(self, solPazienti, indici, statoLavori, statoAmbulatori):
		indAmbulatori = []
		for i in range(3): # Creazione dinamica della lista degli ambulatori in cui controllare i conflitti
			if indici[i] != len(statoAmbulatori[i]):
				indAmbulatori.append(i)

		spostamento = [0, 0, 0] # Spostamento dei job nel caso ci siano conflitti
		
		candidati = {i: min(statoAmbulatori[i][indici[i]]["jobs"].values(), key=lambda x: x.valore).valore for i in indAmbulatori} # Crea un dizionario contenente gli start minimi dei pazienti interessati (volatili)
		while len(candidati) > 0: # Fintanto che ci sono ambulatori con pazienti da controllare
			minAmbulatorio = min(candidati, key=candidati.get) # Indice dell'ambulatorio del candidato che parte prima degli altri
			spostamento[minAmbulatorio] = self.risolviConflitto(solPazienti, statoAmbulatori[minAmbulatorio][indici[minAmbulatorio]], statoLavori, spostamento[minAmbulatorio])

			if indici[minAmbulatorio] == len(statoAmbulatori[minAmbulatorio]) - 1: # Significa che è stato osservato l'ultimo paziente dell'ambulatorio
				indAmbulatori.remove(minAmbulatorio) # Rimozione dell'ambulatorio dalla lista degli ambulatori da controllare
			else:
				indici[minAmbulatorio] += 1
			candidati = {i: min(statoAmbulatori[i][indici[i]]["jobs"].values(), key=lambda x: x.valore).valore for i in indAmbulatori}
	'''
	Risolve i conflitti del paziente in uso.
	Viene esaminato un esame per volta. Subito si sposta l'esame in corso in base agli spostamenti fatti per gli esami precedenti (anche quelli degli altri pazienti) inerenti al medesimo ambulatorio.
	Viene mantenuto l'ordine cronologico degli esami dello stesso tipo e si verificano i vicini di sinistra e destra. Se si trova posto libero, si inserisce l'esame del paziente e si passa al prossimo esame.
	'''
	def risolviConflitto(self, solPazienti, paziente, statoLavori, spostamento):
		for job in paziente["jobs"].items():
			job[1].valore += spostamento # Spostamento è la somma degli spostamenti fatti dei job precedenti del ciclo for

			statoLavori[job[0]-1].sort(key=lambda x: x[1].valore) # Il sorting utilizzato ha la caratteristica di essere stabile
			index = [x[0] for x in statoLavori[job[0]-1]].index(paziente["id"]) # Calcolo posizione paziente nella lista
	
			# Controllo conflitto elemento a sinistra
			if index > 0:
				j = 1
				while index - j >= 0 and solPazienti[statoLavori[job[0]-1][index-j][0]]["volatile"]: # Si cerca il primo job volatile che si trova a sinistra
					j += 1
				if index - j >= 0 and statoLavori[job[0]-1][index-j][1].valore + getattr(self.config, "durata" + str(job[0])) > job[1].valore: # Se la fine del job precedente supera il job attuale
					delta = statoLavori[job[0]-1][index-j][1].valore + getattr(self.config, "durata" + str(job[0])) - job[1].valore # Calcolo spostamento necessario (delta) del job in caso di conflitto
					job[1].valore += delta
					spostamento += delta
					statoLavori[job[0]-1].sort(key=lambda x: x[1].valore) # Il sorting utilizzato ha la caratteristica di essere stabile
					index = [x[0] for x in statoLavori[job[0]-1]].index(paziente["id"]) # Aggiornamento dell'indice
			
			# Controllo conflitto elemento a destra
			if index < len(statoLavori[job[0]-1]) - 1:	
				j = 1
				while index + j < len(statoLavori[job[0]-1]) and job[1].valore + getattr(self.config, "durata" + str(job[0])) > statoLavori[job[0]-1][index+j][1].valore: # Se il job in esame termina dopo l'inizio dell'esame successivo, si ha conflitto
					if not(solPazienti[statoLavori[job[0]-1][index+j][0]]["volatile"]) : # Se il job che crea confitto non è volatile, il conflitto va risolto
						delta = statoLavori[job[0]-1][index+j][1].valore + getattr(self.config, "durata" + str(job[0])) - job[1].valore # Spostamento in avanti in caso di conflitto
						job[1].valore += delta
						spostamento += delta
						statoLavori[job[0]-1].sort(key=lambda fun: fun[1].valore) # Il sorting utilizzato ha la caratteristica di essere stabile
					j += 1
		paziente["volatile"] = False # Il paziente è permanentemente fissato
		
		return spostamento

	'''
	Per l'ambulatorio corrente viene eseguita una compressione dei pazienti che terminano dopo lo start minimo in cui avviene un cambiamento.
	Un ciclo while ha il compito di determinare il primo paziente che ricade nell'area di compressione (soglia in base allo start minimo dei pazienti spostati), allo stesso tempo tenendo in memoria la fine del paziente precedente.
	Terminato il ciclo, viene avviata la procedura di compattazione per ogni paziente presente dopo l'indice trovato.
	'''
	def compattaAmbulatorio(self, listaPazienti, startMin):
		index = 0	# Indice nella lista dei pazienti
		posizioneInserimento = None # Offset di inserimento in caso di compattazione paziente. Coincide con la fine del paziente precedente

		# Il ciclo ha il compito di trovare il primo paziente che si trova nell'area di compressione
		chiaveMaxStart = max(listaPazienti[index]["jobs"], key=lambda x: listaPazienti[index]["jobs"][x].valore) # Chiave del job che inizia più tardi
		while index < len(listaPazienti) and listaPazienti[index]["jobs"][chiaveMaxStart].valore + getattr(self.config, "durata" + str(chiaveMaxStart)) <= startMin: # Se ci sono pazienti e la fine edl job massimo è più piccola della soglia, il paziente va saltato
			listaPazienti[index]["volatile"] = False # Il paziente viene considerato fisso
			posizioneInserimento = listaPazienti[index]["jobs"][chiaveMaxStart].valore + getattr(self.config, "durata" + str(chiaveMaxStart))
			index += 1
			if index < len(listaPazienti):
				chiaveMaxStart = max(listaPazienti[index]["jobs"], key=lambda x: listaPazienti[index]["jobs"][x].valore)
		
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
		paziente["volatile"] = True
		for job in paziente["jobs"].items():
			if job[1].valore < sogliaStart:
				posizioneInserimento = job[1].valore + getattr(self.config, "durata" + str(job[0])) # Calcolo fine del job attuale
			else:
				job[1].valore = posizioneInserimento
				posizioneInserimento += getattr(self.config, "durata" + str(job[0]))
		return posizioneInserimento

	'''
	Funzione per scambiare le posizioni di due pazienti casuali.
	Inizialmente si determinano quali pazienti utilizzare per lo scambio (si considerano le strutture dati complete dei pazienti, non solo gli indici)
	Vengono poi estratte le posizioni dei due pazienti dai rispettivi ambulatori, in modo che successivamente si possa alterare la loro ubicazione nella struttura dati degli ambulatori.
	Infine si scambia il dato che indica dove si trovano i pazienti.
	'''
	def swapPazienti(self, solPazienti, statoAmbulatori):
		# Estrazione casuale pazienti
		paziente1 = choice(solPazienti)
		paziente2 = choice(solPazienti)
		while paziente2 == paziente1:
			paziente2 = choice(solPazienti)

		# Estrapolazione posizione pazienti nella struttura ambulatori
		index1 = statoAmbulatori[paziente1["ambulatorio"]].index(paziente1)
		index2 = statoAmbulatori[paziente2["ambulatorio"]].index(paziente2) 
		
		# Scambio strutture dati
		temp = statoAmbulatori[paziente1["ambulatorio"]][index1]
		statoAmbulatori[paziente1["ambulatorio"]][index1] = statoAmbulatori[paziente2["ambulatorio"]][index2]
		statoAmbulatori[paziente2["ambulatorio"]][index2] = temp

		# Scambio informazione ambulatorio
		tempAmbulatorio = paziente1["ambulatorio"]
		paziente1["ambulatorio"] = paziente2["ambulatorio"]
		paziente2["ambulatorio"] = tempAmbulatorio
		
		return paziente1, paziente2
	
	'''
	Funzione per spostare un paziente casuale in coda ad un ambulatorio casuale
	'''
	def spostamentoPaziente(self, statoAmbulatori):
		randomListIndex = random.randint(0,len(statoAmbulatori)-1)
		randomPersonIndex = random.randint(0,len(statoAmbulatori[randomListIndex])-1)
		persona0 = statoAmbulatori[randomListIndex].pop(randomPersonIndex)
		print(persona0)
		#ora noi abbiamo scelto la nostra persona, dobbiamo scegliere dove andarla a mettere
		#riusiamo randomListIndex
		randomListIndex = random.randint(0,len(statoAmbulatori)-1)
		statoAmbulatori[randomListIndex].append(persona0)
	
	'''
	Funzione per calcolare l'energia di uno stato.
	Il calcolo si basa sulla quantità di spazio non utilizzato che va dall'istante zero, all'istante dell'ultimo ambulatorio che finisce gli esami, ciò definisce una soglia di analisi.
	Non importa se un ambulatorio termina prima dell'istante definito dalla soglia, tutta quest'area viene considerata negativa, in quanto l'ambulatorio potrebbe eseguire degli esami per alleggerire l'ambulatorio che sta ancora lavorando.
	'''
	def energia(self, statoAmbulatori):
		test = [max(statoAmbulatori[i][-1]["jobs"].items(), key=lambda k: k[1].valore) for i in range(3)] # Crea una lista contenente l'ultimo job di ogni ambulatorio
		tipoJob, sogliaStart = max(test, key=lambda k: k[1].valore + getattr(self.config, "durata" + str(k[0]))) # Restituisce due elementi: il tipo di job ed il suo start
		sogliaMax = sogliaStart.valore + getattr(self.config, "durata" + str(tipoJob))

		Etot = 0 # Spazio idle totale

		efficienza = []

		for i in range(3): # Per ogni ambulatorio
			energiaFinale = sogliaMax
			for paziente in statoAmbulatori[i]: # Per ogni paziente
				for job in paziente["jobs"]: # Per ogni job
					energiaFinale -= getattr(self.config, "durata" + str(job))
			efficienza.append((sogliaMax - energiaFinale) / sogliaMax) # Calcolo dell'efficienza di un ambulatorio
			Etot += energiaFinale
		return Etot, efficienza, sogliaMax

	# Simulated Annealing
	def saGraph(self, solPazienti, solJobs, statoAmbulatori, mainWindow):
		#print(ambulatori)
		itera = 0
		calore = self.config.temperatura
		
		vecchiaEnergia, efficienza, sogliaMassima = energia(statoAmbulatori)

		mainWindow.resetGrafico()
		mainWindow.start.setEnabled(False) # Disattivazione tasto start

		mainWindow.widget.creaOggetti(solPazienti, sogliaMassima)
		mainWindow.widgetSolIniziale.creaOggetti(solPazienti, sogliaMassima)
		
		mainWindow.valoreTemperatura.setNum(calore)
		
		mainWindow.maxE.setNum(vecchiaEnergia)
		mainWindow.minE.setNum(vecchiaEnergia)
		mainWindow.energiaSol.setNum(vecchiaEnergia)
		mainWindow.energiaIniziale.setNum(vecchiaEnergia)
		maxE = vecchiaEnergia
		minE = vecchiaEnergia
		
		# Parametri di efficienza ambulatori
		mainWindow.efficienza1.setText("{:.2%}".format(efficienza[0]))
		mainWindow.efficienza2.setText("{:.2%}".format(efficienza[1]))
		mainWindow.efficienza3.setText("{:.2%}".format(efficienza[2]))
		mainWindow.efficienzaMedia.setText("{:.2%}".format((efficienza[0] + efficienza[1] + efficienza[2]) / 3))
		
		mainWindow.efficienza1Iniziale.setText("{:.2%}".format(efficienza[0]))
		mainWindow.efficienza2Iniziale.setText("{:.2%}".format(efficienza[1]))
		mainWindow.efficienza3Iniziale.setText("{:.2%}".format(efficienza[2]))
		mainWindow.efficienzaMediaIniziale.setText("{:.2%}".format((efficienza[0] + efficienza[1] + efficienza[2]) / 3))
		mainWindow.app.processEvents()

		while itera < self.config.iterazioni:# and mainWindow.running:
			calore = calore * self.config.tassoRaffreddamento
			solPazienti_vecchio, jobs_vecchio, ambulatori_vecchio = self.mossa(solPazienti, solJobs, statoAmbulatori)
			nuovaEnergia, efficienza, sogliaMassima = self.energia(statoAmbulatori)
			
			delta = nuovaEnergia - vecchiaEnergia
			# Se la soluzione nuova è migliore o nonostante sia peggiore (non uguale), viene deciso di mantenerla
			if nuovaEnergia < vecchiaEnergia or exp(-(delta)/calore) > uniform(0,1) and delta != 0:
				mainWindow.energiaSol.setNum(nuovaEnergia)
				vecchiaEnergia = nuovaEnergia
				mainWindow.widget.creaOggetti(solPazienti, sogliaMassima)
				
				# Aggiornamento efficienza
				mainWindow.efficienza1.setText("{:.2%}".format(efficienza[0]))
				mainWindow.efficienza2.setText("{:.2%}".format(efficienza[1]))
				mainWindow.efficienza3.setText("{:.2%}".format(efficienza[2]))
				mainWindow.efficienzaMedia.setText("{:.2%}".format((efficienza[0] + efficienza[1] + efficienza[2]) / 3))
			else:
				solPazienti = solPazienti_vecchio
				solJobs = jobs_vecchio
				statoAmbulatori = ambulatori_vecchio

			mainWindow.valoreTemperatura.setNum(calore)


			mainWindow.progressBar.setValue(((itera + 1) / self.config.iterazioni) * 100)
			mainWindow.progressBarLabel.setText("{:.2%}".format((itera + 1) / self.config.iterazioni))
			
			if vecchiaEnergia > maxE:
				mainWindow.maxE.setNum(vecchiaEnergia)
				maxE = vecchiaEnergia
			if vecchiaEnergia < minE:
				mainWindow.minE.setNum(vecchiaEnergia)
				minE = vecchiaEnergia
			mainWindow.draw(self.config.iterazioni - (itera + 1), vecchiaEnergia) # Disegno andamento energia
			
			mainWindow.app.processEvents()
			itera += 1
		return solPazienti
	
	'''
	Funzione principale del Simulated Annealing.
	L'algoritmo crea una nuova soluzione applicando una "mossa" (scambio di pazienti o spostamento di un singolo paziente in coda ad un amvbulatorio) alla soluzione attuale, successivamente compara l'energia delle due soluzioni:
	-	Se la nuova energia è minore, significa che nella nuova soluzione sono presenti meno zone "idle", indicando una miglioria nella soluzione attuale.
	-	Se la nuova energia è maggiore, significa che la soluzione appena trovata è peggiore della precedente, quindi l'algoritmo sceglie se mantenerla ugualmente o scartarla in maniera definitiva. Per farlo, utilizza una formula per definire la probabilità
		di mantenerla ugualmente (exp(- delta / temperatura)).
	Queste scelte si ripetono ad ogni iterazione, fino al raggiungimento della soglia impostata dall'utente. A questo punto viene ritornata la soluzione finale, quella che alla fine risulta con l'energia minore.
	'''
	def sa(self, soluzioneCorrente):
		itera = 0;
		calore = self.config.temperatura
		
		vecchiaEnergia, efficienza, sogliaMassima = self.energia(soluzioneCorrente[2])
		while itera < self.config.iterazioni:
			calore = calore * self.config.tassoRaffreddamento
			soluzioneNuova = self.mossa(soluzioneCorrente)
			nuovaEnergia, efficienza, sogliaMassima = self.energia(soluzioneNuova[2])
			
			# Se la soluzione nuova è migliore o nonostante sia peggiore, viene deciso di mantenerla, sostituendo la vecchia energia e soluzione
			if nuovaEnergia <= vecchiaEnergia or exp(-(nuovaEnergia - vecchiaEnergia)/calore) > uniform(0, 1):
				vecchiaEnergia = nuovaEnergia
				soluzioneCorrente = soluzioneNuova
			itera += 1
		return soluzioneCorrente