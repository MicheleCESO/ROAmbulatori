from copy import deepcopy

class PathRelinking():
	def __init__(self, config):
		self.config = config

	def test(self, soluzione):
		print("\n")
		for paz in soluzione.pazienti:
			paziente = soluzione.pazienti[paz] 
			print(paziente.id,soluzione.ambulatori[paziente.ambulatorio][paziente.posizione].id)
		print("\n")

	def main(self, soluzioneIniziale, soluzioneFinale):
		# Inizializzazione soluzione migliore
		if soluzioneFinale.energia <= soluzioneIniziale.energia:
			soluzioneMigliore = soluzioneFinale
		else:
			soluzioneMigliore = soluzioneIniziale

		# Creazione delle nuove soluzioni grazie allo scorrimento dell'array contenente tutte le soluzioni future (aggiornamento dinamico in loco)
		soluzioneProssimoPasso = soluzioneMigliore
		while soluzioneProssimoPasso:
			soluzioneProssimoPasso, soluzioneMigliore = self.creaSoluzioni(soluzioneProssimoPasso, soluzioneFinale, soluzioneMigliore)

		return soluzioneMigliore


	def creaSoluzioni(self, soluzioneA, soluzioneB, soluzioneMigliore):		
		soluzioneProssimoPasso = None # Soluzione migliore tra tutte quelle qui generate
		# Controllo iterativo sui pazienti, generando nuove soluzioni se i pazienti incontrati risultano fuori posto
		for idPaziente in range(1, len(soluzioneA.pazienti) + 1):
			# Condizione in cui un paziente si trova in una posizione diversa rispetto le due soluzioni
			if soluzioneA.pazienti[idPaziente].ambulatorio != soluzioneB.pazienti[idPaziente].ambulatorio or soluzioneA.pazienti[idPaziente].posizione != soluzioneB.pazienti[idPaziente].posizione:
				nuovaSoluzione, nuovaMatrice = self.generaSoluzione(soluzioneA, idPaziente, soluzioneB)

				# Verifica riguardo le soluzioni figlie della soluzione A
				if soluzioneProssimoPasso == None:
					soluzioneProssimoPasso = nuovaSoluzione
				else:
					if nuovaSoluzione.energia < soluzioneProssimoPasso.energia:
						soluzioneProssimoPasso = nuovaSoluzione
				
				# Verifica riguardo alla bontà della nuova soluzione rispetto la migliore finora
				if nuovaSoluzione.energia < soluzioneMigliore.energia:
					soluzioneMigliore = nuovaSoluzione

		return soluzioneProssimoPasso, soluzioneMigliore

	def generaSoluzione(self, soluzioneA, idPaziente, soluzioneB):
		soluzioneCopia = deepcopy(soluzioneA)
		pazienteA = soluzioneCopia.pazienti[idPaziente] #Estrazione paziente dalla soluzione A
		pazienteB = soluzioneB.pazienti[idPaziente] #Estrazione paziente dalla soluzione B
		if len(soluzioneCopia.ambulatori[pazienteB.ambulatorio]) <= pazienteB.posizione: # Il paziente occupa una posizione che non esiste nella soluzione B. Lo si aggiunge in coda
			startPazienteA = min(pazienteA.esami.values(), key=lambda x: x.valore).valore
			
			posizioneRealePaziente = self.spostaPaziente(pazienteA, pazienteB, soluzioneCopia, soluzioneB)
			
			if posizioneRealePaziente < 0: # Caso in cui il paziente precedente non esiste
				startMin = 0
			else: # Il paziente precedente esiste
				pazientePrecedente = soluzioneCopia.ambulatori[pazienteB.ambulatorio][posizioneRealePaziente]
				tipoEsameMax, ultimoEsamePazientePrecedente = max(pazientePrecedente.esami.items(), key=lambda x: x[1].valore + getattr(self.config, "durata" + str(x[0])))
				finePazientePrecedente = ultimoEsamePazientePrecedente.valore + getattr(self.config, "durata" + str(tipoEsameMax))
				startMin = min(startPazienteA, finePazientePrecedente)
		else:
			# Questo controllo serve per identificare i buchi lasciate nelle liste a causa di pazienti mancanti (la posizione nella lista è diversa dalla posizione del paziente)
			if soluzioneCopia.ambulatori[pazienteB.ambulatorio][pazienteB.posizione].posizione != pazienteB.posizione:
				startPazienteA = min(pazienteA.esami.values(), key=lambda x: x.valore).valore
			
				posizioneRealePaziente = self.spostaPaziente(pazienteA, pazienteB, soluzioneCopia, soluzioneB)
			
				if posizioneRealePaziente < 0: # Caso in cui il paziente precedente non esiste
					startMin = 0
				else: # Il paziente precedente esiste
					pazientePrecedente = soluzioneCopia.ambulatori[pazienteB.ambulatorio][posizioneRealePaziente]
					tipoEsameMax, ultimoEsamePazientePrecedente = max(pazientePrecedente.esami.items(), key=lambda x: x[1].valore + getattr(self.config, "durata" + str(x[0])))
					finePazientePrecedente = ultimoEsamePazientePrecedente.valore + getattr(self.config, "durata" + str(tipoEsameMax))
					startMin = min(startPazienteA, finePazientePrecedente)
			else:
				# Scambio di pazienti con gli indici esistenti. Il paziente C è il paziente che viene scamviato con quello in esame (pazienteA)
				pazienteC = soluzioneCopia.ambulatori[pazienteA.ambulatorio][pazienteA.posizione] = soluzioneCopia.ambulatori[pazienteB.ambulatorio][pazienteB.posizione]
				soluzioneCopia.ambulatori[pazienteB.ambulatorio][pazienteB.posizione] = pazienteA

				pazienteC.posizione = pazienteA.posizione
				pazienteC.ambulatorio = pazienteA.ambulatorio

				pazienteA.posizione = pazienteB.posizione
				pazienteA.ambulatorio = pazienteB.ambulatorio
				pazienteA.ordineEsami = pazienteB.ordineEsami

				startMin = min(list(pazienteA.esami.values()) + list(pazienteC.esami.values()), key=lambda x: x.valore).valore
		
		# Operazioni per risolvere tutti i conflitti
		indiciPazienti = soluzioneCopia.compattaAmbulatori(startMin)
		soluzioneCopia.controlloConflitto(indiciPazienti)

		# Creazione matrice per comparazione soluzioni
		matrice = soluzioneCopia.generaMatricePosizione(soluzioneCopia.ambulatori)
		return soluzioneCopia, matrice

	def spostaPaziente(self, pazienteA, pazienteB, soluzioneA, soluzioneB):
		soluzioneA.ambulatori[pazienteA.ambulatorio].remove(pazienteA)

		# Aggiornamento posizione dei pazienti che venogno dopo il paziente eliminato (solo quelli che non sono stati ancora guardati)
		indice = pazienteA.posizione
		for paziente in soluzioneA.ambulatori[pazienteA.ambulatorio][pazienteA.posizione:]:
			if not paziente.pathRelinkingOsservato: # Le posizioni cambiano solo per i pazienti non osservati, in quanto le loro posizioni devono combaciare con la posizione attuale nell'ambulatorio della soluzione A
				paziente.posizione -= 1

		# Aggiornamento posizioni
		indiceControllo = len(soluzioneA.ambulatori[pazienteB.ambulatorio]) - 1
		while indiceControllo >= 0 and soluzioneA.ambulatori[pazienteB.ambulatorio][indiceControllo].posizione > pazienteB.posizione:
			indiceControllo -= 1
		
		# Aggiornamento informazioni paziente (pazienteA ---> pazienteB)
		pazienteA.posizione = pazienteB.posizione
		pazienteA.ambulatorio = pazienteB.ambulatorio
		pazienteA.ordineEsami = pazienteB.ordineEsami

		# Inserimento paziente in ambulatorio
		soluzioneA.ambulatori[pazienteB.ambulatorio].insert(indiceControllo + 1, pazienteA)
		
		pazienteA.pathRelinkngOsservato = True

		return indiceControllo