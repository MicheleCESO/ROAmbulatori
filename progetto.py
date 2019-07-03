from IstGen import genIstanza
import itertools

pi = [1,2,3,4,5]

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

	startP = [0] * len(ist) # Start pazienti
	startJ = [{}] * len(ist) # I dizionari devono essere separati
	stanzeLibere = 3
	statoStanze = [0,0,0]
	index = 1

	listaPazienti = []

	#statoStanze[minimo] += sum(ist[0])


		while :
			conflitto,lista = confronto(ist,startP,listaPazienti,index) # Confrontiamo paziente scelto attuale con quelli precedentemente scelti
			index += 1
		minimo = minStato(statoStanze)



# Gestisce il confronto tra i pazienti già inseriti e uno nuovo
def confronto(istanza, startPaziente, pazientiInAmbulatorio, nuovoPaziente):

	# Permutazioni possibili del nuovo paziente	
	lista3 = permuta(istanza[nuovoPaziente])
	if len(pazientiInAmbulatorio) == 0:
		return 0,istanza[nuovoPaziente]
	elif len(pazientiInAmbulatorio) == 1:
		lista2 = None
 
 	costo = 9999
 	sol = None
	for p3 in lista3:  
		livelloConflitto = verifica(istanza[pazientiInAmbulatorio[0]],lista2,p3)
		if livelloConflitto < costo:
			costo = livelloConflitto
			sol = p3

	return costo,sol

def verifica(L1,L2,L3):
	for el1 in L1:
		if el1 in L3: # Se ci sono due esami dello stesso tipo

	if L2:		



paziente = MCP(ist)

# Generazione istanza casuale
ist = genIstanza()
pprint(ist)
paziente = MCP(ist)
print(paziente)