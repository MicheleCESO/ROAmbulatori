#import config
#from os.path import isfile
#from IstGen import genIstanza
#from disegno import disegna
#import SA
from random import choice
from valore import Valore

class Greedy():

	def __init__(self, config):
		self.config = config

	def nuovaGreedy(self, istanza, boolGrasp=True):
		startAmbulatori = [0,0,0] # Momento libero per ogni ambulatorio

		pazienti = {} # Struttura contenente informazioni sui lavori di tutti i pazienti
		lavori = [[] for _ in range(5)] # Ogni sottolista contiene un elenco di start di un certo tipo di lavoro.
										 # Questi sono i lavori che sono stati assegnati agli ambulatori
		ambulatori = [[] for _ in range(3)] # Liste contenenti i pazienti in ordine cronologico per ogni ambulatorio
		
		# Creazione ordine di visita in bse al tipo di greedy in uso
		if self.config.greedy == "LPT":
			vettoreIndici = self.LPTGreedy(istanza)
		elif self.config.greedy == "SPT":
			vettoreIndici = self.SPTGreedy(istanza)
		else:
			vettoreIndici = self.FIFOGreedy(istanza)
		print(istanza,"\n\n" ,vettoreIndici)
		for indicePaziente in vettoreIndici:
			print("Stato ambulatori: ", startAmbulatori)
		# Inizializzazione dizionario del nuovo paziente, inserendo anche la voce dei vari jobs. La chiave del dizionario corrisponde all'id del paziente
			pazienti[indicePaziente + 1] = {"jobs": {}}
			
			# Uso random per GRASP, scelta casuale tra i due ambulatori migliori
			if boolGrasp:
				idAmbulatorio = self.sceltaGrasp(startAmbulatori)
			else: # GRASP disattivata
				idAmbulatorio = startAmbulatori.index(min(startAmbulatori))
			
			# Ampliamento della voce paziente, inserendo anche l'ambulatorio, l'id paziente e la durata totale degli esami
			pazienti[indicePaziente + 1]["ambulatorio"] = idAmbulatorio
			pazienti[indicePaziente + 1]["id"] = indicePaziente + 1
			pazienti[indicePaziente + 1]["durataTotale"] = 0
			
			# Inserimento dell'intera voce del paziente nella lista degli ambulatori. Viene creato un riferimento tra le due strutture dati primarie
			ambulatori[idAmbulatorio].append(pazienti[indicePaziente + 1])
			
			# Ciclo sugli esami del paziente
			for idLavoro in istanza[indicePaziente]:
				pazienti[indicePaziente + 1]["durataTotale"] += getattr(self.config, "durata" + str(idLavoro))
				pazienti[indicePaziente + 1]["jobs"][idLavoro] = [] # Uso di liste per sfruttare il riferimento all'oggetto, permette un rapido aggiornamento dei parametri

				startAmbulatori[idAmbulatorio] = self.aggiungiTask(pazienti[indicePaziente + 1]["jobs"], indicePaziente + 1, lavori[idLavoro - 1], startAmbulatori[idAmbulatorio], idLavoro)
			
			#pazienti[indicePaziente + 1]["start"] = min(list(pazienti[indicePaziente + 1]["jobs"].values()), key=lambda f: f.valore) # Salvataggio del parametro start paziente
			print("Paziente ",indicePaziente," inserito nell'ambulatorio ",idAmbulatorio,", jobs: ")
			for k,v in pazienti[indicePaziente + 1]["jobs"].items():
				print(k,v.valore)
		return [pazienti, lavori, ambulatori]

	'''
	Longest Processing Time. Questa greedy sceglie il paziente che occupa più a lungo gli ambulatori e lo assegna al primo disponibile.
	Ad ogni passo si riduce la lista dei pazienti da poter scegliere.
	'''
	def LPTGreedy(self, istanza):
		print("ciaO")
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
	def aggiungiTask(self, jobs, idPaziente, lavori, startAmbulatori, idLavoro):
		durata = getattr(self.config, "durata" + str(idLavoro)) # Estrazione dinamica della durata del task
		
		if len(lavori) > 0: # Se esiste almeno un altro job dello stesso tipo, si verifica se ci sono conflitti
			index = 0
			spazioNonTrovato = True
			while index < len(lavori) and spazioNonTrovato: # Ciclo dei job per cercare la posizione in cui inserire quello nuovo
				[nuovostartAmbulatori, spazioNonTrovato] = self.controlloProssimoJob(startAmbulatori, durata, lavori[index][1].valore)  # Aggiunta dell'indice zero per accedere al valore nella lista contenente il singolo valore.
				if spazioNonTrovato:
					startAmbulatori = nuovostartAmbulatori
					index += 1

		jobs[idLavoro] = Valore(startAmbulatori)
		lavori.append([idPaziente, jobs[idLavoro]])
		lavori.sort(key=lambda x: x[1].valore)

		return startAmbulatori + durata # Ritorno il nuovo startAmbulatori dell'ambulatorio

	# Verifica dei casi possibili: il job osservato è presente (conflitto in atto), futuro (deve ancora incominciare), passato (è già terminato).
	def controlloProssimoJob(self, startAmbulatori, durata, startJob):
		if startAmbulatori + durata > startJob and startJob + durata > startAmbulatori: # Condizione di conflitto
			spazioNonTrovato = True
			return [startJob + durata, spazioNonTrovato] # startAmbulatori posizionato alla fine del task a destra
		else:
			if startAmbulatori < startJob: # Sto controllando un job che viene dopo, senza conflitti, quindi posso inserire il nuovo job nel suo startAmbulatori
				spazioNonTrovato = False
				return [startAmbulatori, spazioNonTrovato]
			else: # Il job in analisi è da ignorare in quanto è già terminato all'istante segnato da startAmbulatori
				spazioNonTrovato = True
				return [startAmbulatori, spazioNonTrovato]

def main(mainWindow=None):
	#ist = genIstanza(conf["Istanze"])
	ist = [[5], [5], [2, 4, 5, 1], [3], [5, 2], [4], [5, 2], [2, 3, 1, 5], [2], [1], [5, 3, 1], [5], [1, 4], [4], [1, 2, 3]]
	print(ist,"\n\n")
	durata = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
	pazienti, jobs, ambulatori = euri(ist, durata, True)
	disegna(pazienti, durata)
	res = SA.sa(pazienti, jobs, ambulatori, mainWindow.config, mainWindow)
	
	disegna(pazienti, durata)

if __name__ == "__main__":
	main()
