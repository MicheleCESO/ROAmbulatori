import config
from os.path import isfile
from IstGen import genIstanza
from disegno import disegna
import SA

def euri(ist, durata):
	offset = [0,0,0] # Momento libero per ogni ambulatorio

	pazienti = {} # Struttura contenente informazioni sui lavori di tutti i pazienti
	jobList = [[] for _ in range(5)] # Ogni sottolista contiene un elenco di start di un certo tipo di lavoro.
									 # Questi sono i lavori che sono stati assegnati agli ambulatori
	ambulatori = [[] for _ in range(3)] # Liste contenenti i pazienti in ordine cronologico per ogni ambulatorio
	i = 1
	for paziente in ist:
		pazienti[i] = {"jobs": {}}
		idAmbulatorio = offset.index(min(offset))
		pazienti[i]["ambulatorio"] = idAmbulatorio
		pazienti[i]["id"] = i
		ambulatori[idAmbulatorio].append(pazienti[i])
		print("dsdasd ",paziente)
		for idJob in paziente:
			pazienti[i]["jobs"][idJob] = [] # Uso di liste per sfruttare il riferimento all'oggetto, permette un rapido aggiornamento dei parametri

			nuovoOffset = aggiungiTask(pazienti[i]["jobs"][idJob], i, jobList[idJob - 1], offset[idAmbulatorio], durata[idJob])
			print(offset[idAmbulatorio],"- -",nuovoOffset)
			offset[idAmbulatorio] = nuovoOffset
		pazienti[i]["start"] = min(list(pazienti[i]["jobs"].values()))[0] # Salvataggio del parametro start paziente
		i += 1
	return pazienti, jobList, ambulatori

def aggiungiTask(job, idPaziente, jobList, offset, durata):
	allarme = False
	if len(jobList) > 0:
		index = 0
		spazioNonTrovato = True
		while index < len(jobList) and spazioNonTrovato:
			[nuovoOffset, allarme] = controlloProssimoJob(offset, durata, jobList[index][1][0], allarme)  # Aggiunta dell'indice zero per accedere al valore nella lista
																			# contenente il singolo valore.
			
			if offset == nuovoOffset: # Se gli offset coincidono significa che il job ci sta e termino, altrimenti tento con il job successivo
				if allarme:
					spazioNonTrovato = False
				else:
					index += 1
			else:
				offset = nuovoOffset
				index += 1
	jobList.append([idPaziente, job]) # Inseriamo il job nella lista di supporto come lista, così il valore viene automaticamente aggiornato
	job.append(offset) # Append perchè il valore usa una lista come incapsulamento
	jobList.sort(key=lambda fun: fun[1][0]) # Riordino dei job in senso crescente

	return offset + durata # Ritorno il nuovo offset dell'ambulatorio

# Allarme rimane false fintanto che analizzo job che finiscono prima che incominci quello attuale, al primo job con cui ha conflitto, si setta
# a true. La prossima volta che non trova conflitto, significa che trova il posto in cui inserirsi
def controlloProssimoJob(offset, durata, startJob, allarme):
	if offset + durata > startJob and startJob + durata > offset: # Condizione di conflitto
		return [startJob + durata, True] # Offset posizionato alla fine del task a destra
	else:
		if offset < startJob: # Sto controllando un job che viene dopo, senza conflitti, quindi posso inserire il nuovo job nel suo offset
			return [offset, True]
		else: # Il job in analisi è da ignorare in quanto è già terminato all'istante segnato da offset
			return [offset, allarme]

def printt(istanza):
	print("\n########\n")
	for e,v in istanza.items():
		print(e,v)
	print("\n########")

def main(mainWindow=None):
	#ist = genIstanza(conf["Istanze"])
	ist = [[5], [5], [2, 4, 5, 1], [3], [5, 2], [4], [5, 2], [2, 3, 1, 5], [2], [1], [5, 3, 1], [5], [1, 4], [4], [1, 2, 3]]
	print(ist,"\n\n")
	durata = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
	pazienti, jobs, ambulatori = euri(ist, durata)
	#printt(pazienti)
	#print(jobs)
	#print(ambulatori)
	disegna(pazienti, durata)
	#for _ in range(4):
		#SA.mossa(pazienti, jobs, ambulatori)
	res = SA.sa(pazienti, jobs, ambulatori, mainWindow.config, mainWindow)
	
	#res = SA.sa(pazienti, jobs, ambulatori, mainWindow.config.temperatura, mainWindow.config.iterazioni, mainWindow.config.tassoRaffreddamento, mainWindow)
		#printt(pazienti)
	disegna(pazienti, durata)

if __name__ == "__main__":
	main()
