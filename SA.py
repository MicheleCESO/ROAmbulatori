from math import exp		# Per l'esponenziale e
from random import uniform	# Per generare numeri pseudocasuali (0,1)
from random import shuffle,randint,choice
from progetto import pi
from disegno import disegna
from copy import deepcopy

# Funzione per generare un vicino da confrontare con lo stato attuale:
# 1 - selezione pseudocasuale di due pazienti diversi.
# 2 - selezione dello start minimo, che comporta una compattazione nei 3 ambulatori (dallo start minimo fino al punto più lontano)
def mossa(statoIniziale, statoLavori, statoAmbulatori):
	statoIniziale_copia, statoLavori_copia, statoAmbulatori_copia = deepcopy([statoIniziale, statoLavori, statoAmbulatori]) # Copia dello stato attuale
	paziente1, paziente2 = sceltaSwapPazienti(statoIniziale, statoAmbulatori) # 1

	startMin = min(list(paziente1["jobs"].values()) + list(paziente2["jobs"].values()))[0] # 2

	# Compattamento degli ambulatori nell'area che inizia con lo start minimo dei pazienti scambiati
	indici = [0,0,0] # Indici dei pazienti da cui partire per verificare i conflitti
	for i in range(3):
		indici[i] = compattaAmbulatorio(statoAmbulatori[i], startMin)
	
	controlloConflitto(statoIniziale, indici, statoLavori, statoAmbulatori)

	return [statoIniziale_copia, statoLavori_copia, statoAmbulatori_copia]

# Questa funzione controlla se ci sono conflitti tra i vari pazienti e li risolve spostandoli
def controlloConflitto(statoIniziale, indici, statoLavori, statoAmbulatori):
	ind = [0, 1, 2] # Indici degli ambulatori che contengono ancora pazienti da controllare
	spostamento = [0, 0, 0] # Spostamento dei job nel caso ci siano conflitti

	candidati = {i: min(statoAmbulatori[i][indici[i]]["jobs"].values()) for i in ind} # Crea un dizionario contenente gli start minimi dei pazienti interessati
	while len(candidati) > 0: # Fintanto che ci sono ambulatori con pazienti da controllare
		minPaziente = min(candidati, key=candidati.get) # Indice del paziente che parte prima degli altri
		spostamento[minPaziente] = risolviConflitto(statoIniziale, statoAmbulatori[minPaziente][indici[minPaziente]], statoLavori, spostamento[minPaziente])

		if indici[minPaziente] == len(statoAmbulatori[minPaziente]) - 1: # Significa che è stato osservato l'ultimo paziente dell'ambulatorio
			ind.remove(minPaziente) # Rimozione dell'ambulatorio dalla lista degli ambulatori da controllare
		else:
			indici[minPaziente] += 1
		candidati = {i: min(statoAmbulatori[i][indici[i]]["jobs"].values())[0] for i in ind}

# Risolve i conflitti del paziente in uso
def risolviConflitto(statoIniziale, paziente, statoLavori, spostamento):
	daAggiornare = False
	for job in paziente["jobs"].items():
		job[1][0] += spostamento
		statoLavori[job[0]-1].sort(key=lambda fun: fun[1][0]) # Riordino dei job in senso cronologico

		index = [x[0] for x in statoLavori[job[0]-1]].index(paziente["id"])
		
		# Controllo conflitto elemento a sinistra
		if index > 0:
			j = 1
			while index - j >= 0 and statoIniziale[statoLavori[job[0]-1][index-j][0]]["volatile"]:
				j += 1
			if index - j >= 0 and statoLavori[job[0]-1][index-j][1][0] + pi[job[0]] > job[1][0] and not(statoIniziale[statoLavori[job[0]-1][index-j][0]]["volatile"]): # Se la fine del job precedente supera il job attuale
				spostamento2 = statoLavori[job[0]-1][index-j][1][0] + pi[job[0]] - job[1][0] # Spostamento del job in caso di conflitto
				job[1][0] += spostamento2
				spostamento += spostamento2
				daAggiornare = True
				statoLavori[job[0]-1].sort(key=lambda fun: fun[1][0])
				index = [x[0] for x in statoLavori[job[0]-1]].index(paziente["id"])
			# while index - j >= 0 and statoLavori[job[0]-1][index-j][1][0] == statoLavori[job[0]-1][index-1][1][0]:
			# 	if paziente["id"]==7:
			# 		print("while: ",statoLavori[job[0]-1][index-j][1][0] + pi[job[0]],job[1][0],not(statoIniziale[statoLavori[job[0]-1][index-j][0]]["volatile"]),statoLavori[job[0]-1][index-j][0],statoLavori[job[0]-1][index-j][1])
			# 	if statoLavori[job[0]-1][index-j][1][0] + pi[job[0]] > job[1][0] and not(statoIniziale[statoLavori[job[0]-1][index-j][0]]["volatile"]): # Se la fine del job precedente supera il job attuale
			# 		spostamento2 = statoLavori[job[0]-1][index-1][1][0] + pi[job[0]] - job[1][0] # Spostamento del job in caso di conflitto
			# 		job[1][0] += spostamento2
			# 		spostamento += spostamento2
			# 		daAggiornare = True
			# 		statoLavori[job[0]-1].sort(key=lambda fun: fun[1][0])
			# 	j += 1
		
		# Controllo conflitto elemento a destra
		if index < len(statoLavori[job[0]-1]) - 1:	
			j = 1
			# while index + j < len(statoLavori[job[0]-1]) and statoIniziale[statoLavori[job[0]-1][index+j][0]]["volatile"]:
			# 	j += 1
			# print(len(statoLavori[job[0]-1]),index+j,index,j)
			
			# if index + j < len(statoLavori[job[0]-1]) and job[1][0] + pi[job[0]] > statoLavori[job[0]-1][index+j][1][0] and not(statoIniziale[statoLavori[job[0]-1][index+j][0]]["volatile"]): # Se la fine del job attuale supera l'inizio del job successivo
			# 	spostamento2 = statoLavori[job[0]-1][index+j][1][0] + pi[job[0]] - job[1][0] # Spostamento in avanti in caso di conflitto
			# 	job[1][0] += spostamento2
			# 	spostamento += spostamento2
			# 	daAggiornare = True
			# 	statoLavori[job[0]-1].sort(key=lambda fun: fun[1][0])
			# 	index = [x[0] for x in statoLavori[job[0]-1]].index(paziente["id"])
			while index + j < len(statoLavori[job[0]-1]) and abs(statoLavori[job[0]-1][index+j][1][0] - job[1][0]) < pi[job[0]]:
				if not(statoIniziale[statoLavori[job[0]-1][index+j][0]]["volatile"]) : # Se la fine del job attuale supera l'inizio del job successivo
					spostamento2 = statoLavori[job[0]-1][index+j][1][0] + pi[job[0]] - job[1][0] # Spostamento in avanti in caso di conflitto
					job[1][0] += spostamento2
					spostamento += spostamento2
					daAggiornare = True
					statoLavori[job[0]-1].sort(key=lambda fun: fun[1][0])
				j += 1
	paziente["volatile"] = False
	
	return spostamento

# Per l'ambulatorio corrente viene eseguita una compressione dei pazienti che terminano dopo lo start minimo in cui avviene un cambiamento
def compattaAmbulatorio(listaPazienti, startMin):
	offset = startMin	# Punto di inizio per la compressione
	index = 0	# Indice nella lista dei pazienti

	# Il ciclo ha il compito di trovare il primo paziente che si trova nell'area di compressione
	chiaveMaxStart = max(listaPazienti[index]["jobs"], key=listaPazienti[index]["jobs"].get) # Job che inizia più tardi
	#print(listaPazienti[index]["jobs"][chiaveMaxStart],pi)
	while index < len(listaPazienti) and listaPazienti[index]["jobs"][chiaveMaxStart][0] + pi[chiaveMaxStart] <= startMin:
		listaPazienti[index]["volatile"] = False # Il paziente viene considerato fisso e causa di possibili conflitti
		index += 1
		if index < len(listaPazienti):
			chiaveMaxStart = max(listaPazienti[index]["jobs"], key=listaPazienti[index]["jobs"].get)
	if index == len(listaPazienti):
		index -= 1
	
	# Ora sono presenti solo pazienti che sono di tipo volative, ovvero soggetti a modifica delle tempistiche
	for paziente in listaPazienti[index:]:
		offset = compattaPaziente(paziente, startMin, offset)

	return index

def compattaPaziente(paziente, startMin, offset):
	paziente["volatile"] = True # Il paziente non causa conflitti se è volatile, va ignorato
	for job in paziente["jobs"].items():
		if job[1][0] >= startMin:
			job[1][0] = offset
			offset += pi[job[0]] 
		else:
			# Se il job supera la soglia minima, aggiorno l'offset
			if job[1][0] + pi[job[0]] > startMin:
				offset = job[1][0] + pi[job[0]]
	return offset

# Scelta di due pazienti sempre diversi
def sceltaSwapPazienti(stato, ambulatori):
	global vi,scell
	p1 = choice(list(stato))
	p2 = choice(list(set(stato) - set([p1]))) # Operazione di differenza (insiemi) per generare una lista che non contenga l'elemento p1
	
	#p1 = scell[vi][0]
	#p2 = scell[vi][1]
	#vi +=1

	#print("swap: ",p1, p2)
	swapPazienti(ambulatori, stato[p1], stato[p2])
	return stato[p1],stato[p2]

# Esecuzione dello swap tra pazienti
def swapPazienti(ambulatori, paziente1, paziente2):
	# Estrapolazione indici pazienti negli ambulatori
	index1 = ambulatori[paziente1["ambulatorio"]].index(paziente1)
	index2 = ambulatori[paziente2["ambulatorio"]].index(paziente2) 
	
	# Scambio strutture dati

	temp = ambulatori[paziente1["ambulatorio"]][index1]
	ambulatori[paziente1["ambulatorio"]][index1] = ambulatori[paziente2["ambulatorio"]][index2]
	ambulatori[paziente2["ambulatorio"]][index2] = temp

	tempAmbulatorio = paziente1["ambulatorio"]
	paziente1["ambulatorio"] = paziente2["ambulatorio"]
	paziente2["ambulatorio"] = tempAmbulatorio

	tempStart = paziente1["start"]
	paziente1["start"] = paziente2["start"]
	paziente2["start"] = tempStart

# Funzione per calcolare l'energia di uno stato
def energia(ambulatori):
	test = [max(ambulatori[i][-1]["jobs"].items(), key=lambda k: k[1][0]) for i in range(3)] # Crea una lista contenente l'ultimo job di ogni ambulatorio
	tipoJob, sogliaStart = max(test, key=lambda k: k[1][0] + pi[k[0]]) # Restituisce due elementi: il tipo di job ed il suo start
	sogliaMax = sogliaStart[0] + pi[tipoJob]

	Etot = 0 # Spazio idle totale

	efficienza = []

	for i in range(3): # Per ogni ambulatorio
		energiaFinale = sogliaMax
		for paziente in ambulatori[i]: # Per ogni paziente
			for job in paziente["jobs"]: # Per ogni job
				energiaFinale -= pi[job]
		efficienza.append((sogliaMax - energiaFinale) / sogliaMax) # Calcolo dell'efficienza di un ambulatorio
		print(sogliaMax - energiaFinale,sogliaMax,energiaFinale)
		Etot += energiaFinale
	return Etot, efficienza, sogliaMax

# Simulated Annealing
def saGraph(statoIniziale, jobs, ambulatori, conf, mainWindow):
	print(ambulatori)
	itera = 0
	calore = conf.temperatura
	counterDelta = 1

	vecchiaEnergia, efficienza, sogliaMassima = energia(ambulatori)

	mainWindow.resetGrafico()
	mainWindow.start.setEnabled(False) # Disattivazione tasto start

	mainWindow.widget.creaOggetti(statoIniziale, sogliaMassima)
	mainWindow.widgetSolIniziale.creaOggetti(statoIniziale, sogliaMassima)
	
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

	running = [mainWindow.running]

	while itera < conf.iterazioni:# and mainWindow.running:
		calore = calore * conf.tassoRaffreddamento
		statoIniziale_vecchio, jobs_vecchio, ambulatori_vecchio = mossa(statoIniziale, jobs, ambulatori)
		nuovaEnergia, efficienza, sogliaMassima = energia(ambulatori)
		
		delta = nuovaEnergia - vecchiaEnergia
		# Se la soluzione nuova è migliore o nonostante sia peggiore (non uguale), viene deciso di mantenerla
		if nuovaEnergia < vecchiaEnergia or exp(-(delta)/calore) > uniform(0,1) and delta != 0:
			mainWindow.energiaSol.setNum(nuovaEnergia)
			vecchiaEnergia = nuovaEnergia
			mainWindow.widget.creaOggetti(statoIniziale, sogliaMassima)
			
			# Aggiornamento efficienza
			mainWindow.efficienza1.setText("{:.2%}".format(efficienza[0]))
			mainWindow.efficienza2.setText("{:.2%}".format(efficienza[1]))
			mainWindow.efficienza3.setText("{:.2%}".format(efficienza[2]))
			mainWindow.efficienzaMedia.setText("{:.2%}".format((efficienza[0] + efficienza[1] + efficienza[2]) / 3))
		else:
			statoIniziale = statoIniziale_vecchio
			jobs = jobs_vecchio
			ambulatori = ambulatori_vecchio

		mainWindow.valoreTemperatura.setNum(calore)


		mainWindow.progressBar.setValue(((itera + 1) / conf.iterazioni) * 100)
		mainWindow.progressBarLabel.setText("{:.2%}".format((itera + 1) / conf.iterazioni))
		
		if vecchiaEnergia > maxE:
			mainWindow.maxE.setNum(vecchiaEnergia)
			maxE = vecchiaEnergia
		if vecchiaEnergia < minE:
			mainWindow.minE.setNum(vecchiaEnergia)
			minE = vecchiaEnergia
		mainWindow.draw(conf.iterazioni - (itera + 1), vecchiaEnergia) # Disegno andamento energia
		
		mainWindow.app.processEvents()
		itera += 1
	return statoIniziale
	
def sa(statoIniziale, jobs, ambulatori, conf, mainWindow):

	itera = 0
	calore = conf.temperatura
	solAccettata = None
	counterDelta = 1
	aggiornaEfficienza = 500 # Iterazioni che devono passsare per aggiornare l'efficienza


	vecchiaEnergia = energia(ambulatori)
	if mainWindow is not None:
		mainWindow.resetGrafico()
		mainWindow.start.setEnabled(False) # Disattivazione tasto start
		
		mainWindow.valoreTemperatura.setNum(calore)
		
		mainWindow.maxE.setNum(vecchiaEnergia)
		mainWindow.minE.setNum(vecchiaEnergia)
		maxE = vecchiaEnergia
		minE = vecchiaEnergia
		deltaSommatoria = 0
		
		mainWindow.app.processEvents()
		running = [mainWindow.running]

	while itera < conf.iterazioni:# and mainWindow.running:
		calore = calore * conf.tassoRaffreddamento
		statoIniziale_vecchio, jobs_vecchio, ambulatori_vecchio = mossa(statoIniziale, jobs, ambulatori)
		nuovaEnergia = energia(ambulatori)
		
		# Se la soluzione nuova è migliore o nonostante sia peggiore, viene deciso di mantenerla
		if nuovaEnergia <= vecchiaEnergia or exp(-(nuovaEnergia - vecchiaEnergia)/calore) > uniform(0,1):
			vecchiaEnergia = nuovaEnergia
			solAccettata = True
		else:
			statoIniziale = statoIniziale_vecchio
			jobs = jobs_vecchio
			ambulatori = ambulatori_vecchio
			solAccettata = False
		if mainWindow is not None:
			mainWindow.valoreTemperatura.setNum(calore)
			if solAccettata:
				deltaSommatoria += nuovaEnergia - vecchiaEnergia # Aggiornamento sommatoria per delta medio
				mainWindow.delta.setNum(deltaSommatoria / counterDelta)
				counterDelta += 1
				print(nuovaEnergia, vecchiaEnergia, deltaSommatoria,counterDelta)
			mainWindow.progressBar.setValue(((itera + 1) / conf.iterazioni) * 100)
			mainWindow.progressBarLabel.setText("{:.2%}".format(itera / conf.iterazioni)+ " %")
			
			if vecchiaEnergia > maxE:
				mainWindow.maxE.setNum(vecchiaEnergia)
				maxE = vecchiaEnergia
			if vecchiaEnergia < minE:
				mainWindow.minE.setNum(vecchiaEnergia)
				minE = vecchiaEnergia
			mainWindow.draw(conf.iterazioni - (itera + 1), vecchiaEnergia) # Disegno andamento energia
			
			mainWindow.app.processEvents()
		itera += 1
	return statoIniziale

if __name__ == "__main__":
	statoIniziale = [1,2,3,4,5,6,7,8,0]
	shuffle(statoIniziale)
	print("Situazione iniziale: {}\n".format(statoIniziale))
	c = {"Temperatura":2,"Iterazioni":200000}

	res = sa(statoIniziale,c,0.99)
	
	print(res)
