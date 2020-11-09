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

	def nuovaGreedy(self, ist, boolGrasp=True):
		startAmbulatori = [0,0,0] # Momento libero per ogni ambulatorio

		pazienti = {} # Struttura contenente informazioni sui lavori di tutti i pazienti
		lavori = [[] for _ in range(5)] # Ogni sottolista contiene un elenco di start di un certo tipo di lavoro.
										 # Questi sono i lavori che sono stati assegnati agli ambulatori
		ambulatori = [[] for _ in range(3)] # Liste contenenti i pazienti in ordine cronologico per ogni ambulatorio
		i = 1
		for paziente in ist:
		# Inizializzazione dizionario del nuovo paziente, inserendo anche la voce dei vari jobs
			pazienti[i] = {"jobs": {}}
			
			# Uso random per GRASP, scelta casuale tra i due ambulatori migliori
			if boolGrasp:
				idAmbulatorio = self.sceltaGrasp(startAmbulatori)
			else: # GRASP disattivata
				idAmbulatorio = startAmbulatori.index(min(startAmbulatori))
			
			# Ampliamento della voce paziente, inserendo anche l'ambulatorio e id paziente
			pazienti[i]["ambulatorio"] = idAmbulatorio
			pazienti[i]["id"] = i
			
			# Inserimento dell'intera voce del paziente nella lista degli ambulatori. Viene creato un riferimento tra le due strutture dati primarie
			ambulatori[idAmbulatorio].append(pazienti[i])
			
			for idLavoro in paziente:
				pazienti[i]["jobs"][idLavoro] = [] # Uso di liste per sfruttare il riferimento all'oggetto, permette un rapido aggiornamento dei parametri

				startAmbulatori[idAmbulatorio] = self.aggiungiTask(pazienti[i]["jobs"], i, lavori[idLavoro - 1], startAmbulatori[idAmbulatorio], idLavoro)
			
			pazienti[i]["start"] = min(list(pazienti[i]["jobs"].values()), key=lambda f: f.valore) # Salvataggio del parametro start paziente
			i += 1
		return [pazienti, lavori, ambulatori]

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

		#lavori.append([idPaziente, job]) # Inseriamo il job nella lista di supporto come lista, così il valore viene automaticamente aggiornato
		#job.append(startAmbulatori) # Append perchè il valore usa una lista come incapsulamento
		#lavori.sort(key=lambda fun: fun[1][0]) # Riordino dei job in senso crescente

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
