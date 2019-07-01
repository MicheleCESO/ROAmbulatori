from IstGen import genIstanza

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

	stanzeLibere = 3
	statoStanze = [0,0,0]
	index = 1

	listaPazienti = [ist[0]]

	for :

		minimo = minStato(statoStanze)
		if : # Ho già scelto altri pazienti e devono essere confrontati
			conflitto,lista = confronto(listaPazienti,ist(index)) # Confrontimo paziente scelto attuale con quelli precedentemente scelti
		index += 1
		stanzeLibere -= 1

def confronto(lista,paziente):



paziente = MCP(ist)

# Generazione istanza casuale
ist = genIstanza()
pprint(ist)
paziente = MCP(ist)
print(paziente)