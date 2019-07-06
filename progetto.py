from IstGen import genIstanza
from itertools import permutations as perm

pi = [1,2,3,4,5]

def permuta(lista):
	return list(perm(lista))

def pprint(ist):
	print(ist,"\n")
	for p in ist:
		for p2 in p:
			print(p2,pi[p2-1])

		print("Sum:",sum(p),"\n")

# Massima cardinalità paziente
def MCP(array):
	i = 1 # Indice scorrimento
	sol = 0 # Soluzione finale
	while i < len(array):
		card = len(array[i])
		if len(array[sol]) < card: # Il nuovo paziente ha una cardinalità maggiore
			sol = i
		i += 1

	return sol 

def risolvi(ist):
	# Riordino istanza per cardinalità decrescente
	ist.sort(key=len)
	ist.reverse()
	print(">>>>>>>>",ist)
	startP = [0] * len(ist) # Start pazienti
	startJ = [{} for _ in range(len(ist))] # Ogni dizionario contiene gli start|stop dei jobs di un paziente
	statoStanze = [0,0,0]
	index = 0

	listaPazienti = [] # Pazienti presenti nei laboratori
	gestionePazienti = {} # Dizionario che collega gli indici degli ambulatori agli indici dei pazienti

	indiciUtilizzabili = [i for i in range(len(ist))] # Indici per capire quali pazienti scegliere

	for _ in range(len(ist)):
		minimoConflitto = 999
		minimo = minStato(statoStanze)

		cancellaPazienti(listaPazienti,statoStanze,minimo,gestionePazienti)

		flag = True

		while flag and index < len(ist):
			if index in indiciUtilizzabili:
				print("---",minimo,startJ)
				conflitto, sol = confronto(ist,startJ,listaPazienti,index,statoStanze[minimo[0]]) # Confrontiamo paziente scelto attuale con quelli precedentemente scelti
			
				if conflitto < minimoConflitto:
					minimoConflitto = conflitto
					scelta = sol
				if conflitto == 0:
					flag = False
			index += 1

		# Inserimento in ambulatorio
		listaPazienti.append(index-1)
		ist[index-1] = sol
		gestionePazienti[minimo[0]] = index - 1
		print("***",indiciUtilizzabili,index-1)
		indiciUtilizzabili.remove(index-1) # Cancello elemento già estratto
		listaPazienti[minimo[0]] = index - 1
	return startJ

# Cancella i pazienti che escono dagli ambulatori
def cancellaPazienti(listaPazienti,ambulatori,minimo,collegamento):
	for elm in minimo[::-1]:
		if ambulatori[elm] > 0:
			listaPazienti.remove(collegamento[elm])

# Ritorna gli indici con i valori minimi della lista
def minStato(lista):
	index = []
	minimo = 9999
	for i in range(3):
		if minimo > lista[i]:
			minimo = lista[i]
			index = [i]
		elif minimo == lista[i]:
			index.append(i)
	return index

# Gestisce il confronto tra i pazienti già inseriti e uno nuovo
def confronto(istanza, startJobs, pazientiInAmbulatorio, nuovoPaziente, startNuovo):

	global pi

	# Permutazioni possibili del nuovo paziente	
	lista3 = permuta(istanza[nuovoPaziente])
	if len(pazientiInAmbulatorio) == 0:
		
		# Genero gli start momentanei del nuovo paziente
		startScorr = startNuovo
		for elm in istanza[nuovoPaziente]:
			startJobs[nuovoPaziente][elm] = startScorr
			startScorr += pi[elm-1] # Aggiorno lo start

		return 0,istanza[nuovoPaziente]
	
	elif len(pazientiInAmbulatorio) == 1:
		lista2 = None
		start2 = None
		print("qui")
	else:
		lista2 = istanza[pazientiInAmbulatorio[1]]
		start2 = startJobs[pazientiInAmbulatorio[1]]

	costo = 9999
	for p3 in lista3:
		startJobs[nuovoPaziente] = {} # Resetto gli start del nuovo paziente
		
		# Genero gli start momentanei del nuovo paziente
		startScorr = startNuovo
		for elm in istanza[nuovoPaziente]:
			startJobs[nuovoPaziente][elm] = startScorr
			startScorr += pi[elm-1] # Aggiorno lo start

		print(startJobs)
		livelloConflitto1 = verifica(istanza[pazientiInAmbulatorio[0]],startJobs[pazientiInAmbulatorio[0]],p3,startJobs[nuovoPaziente])
		livelloConflitto2 = verifica(lista2,start2,p3,startJobs[nuovoPaziente])
		
		totaleConflitto = livelloConflitto1 + livelloConflitto2

		if totaleConflitto < costo:
			costo = totaleConflitto
			sol = p3
		if totaleConflitto == 0:
			break

	return costo, sol

def verifica(jobsVecchi,start,jobsNuovi,startNuovo):
	global pi
	conflittoTotale = 0
	print(jobsNuovi,jobsVecchi,start,startNuovo)
	if jobsVecchi == None:
		return conflittoTotale
	for el in jobsNuovi:
		if el in jobsVecchi: # Se ci sono due esami dello stesso tipo
			print("---->",el)
			diff = start[el] - startNuovo[el]
			if abs(diff) < pi[el]: # Conflitto
				conflitto = diff + pi[el-1];print("#",diff,pi[el-1],conflitto)
				
				conflittoTotale += conflitto

				for i in range(jobsNuovi.index(el),len(jobsNuovi)):
					print("*",jobsNuovi[i])
					startNuovo[jobsNuovi[i]] += conflitto
	return conflittoTotale

if __name__ == "__main__":
	#paziente = MCP(ist)
	ist = [[2, 4], [4, 2, 3], [5, 4]]
	print(ist)
	# Generazione istanza casuale
	#ist = genIstanza()
	#print(ist)
	#pprint(ist)
	#paziente = MCP(ist)
	#print(paziente)
	starts = risolvi(ist)
	print(starts)