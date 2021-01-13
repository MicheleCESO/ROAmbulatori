from copy import deepcopy	# Per la copia delle soluzioni
from math import floor		# Per la ricerca dicotomica

class PathRelinking():
	def __init__(self, config):
		self.config = config

	def dive(self,m1,m2):
		for a1 in m1:
			print(a1)
		print("\n")
		for a2 in m2:
			print(a2)

		diversi=0
		for i in range(len(m1)):
			for j in range(len(m1[i])):
				try:
					if m1[i][j] != m2[i][j]:
						diversi+=1
				except IndexError:
						diversi+=1
		return diversi

	def test(self, soluzione):
		print("\n")
		for paz in soluzione.pazienti:
			paziente = soluzione.pazienti[paz] 
			print(paziente.id,soluzione.ambulatori[paziente.ambulatorio][paziente.posizione].id)
		print("\n")

	def main(self, soluzioneIniziale, soluzioneFinale):
		print("\n\n\n\n")
		listaSoluzioni = [soluzioneIniziale] # Lista ordinata delle soluzioni (pool)
		listaMatrici = [soluzioneIniziale.generaMatricePosizione()]	# Lista ordinata delle posizioni dei pazienti per ogni soluzione
		soluzioneIniziale.livello=0
		# Inizializzazione soluzione migliore
		if soluzioneFinale.energia <= soluzioneIniziale.energia:
			soluzioneMigliore = soluzioneFinale
		else:
			soluzioneMigliore = soluzioneIniziale
		i=0
		while len(listaSoluzioni) > 0:
			prossimaSoluzione = listaSoluzioni.pop(0) # Estrazione prossima soluzione da espandere
			del listaMatrici[0]
			print(10000000-len(listaSoluzioni))
			soluzioneMigliore, listaSoluzioni, listaMatrici ,i= self.creaSoluzioni(listaSoluzioni, listaMatrici, prossimaSoluzione, soluzioneFinale, soluzioneMigliore,i)
		return soluzioneMigliore

	'''
	Funzione che crea le soluzioni di una mossa più vicine alla soluzione B.
	'''
	def creaSoluzioni(self, listaSoluzioni, listaMatrici, soluzioneA, soluzioneB, soluzioneMigliore,i):		
		# Controllo iterativo sui pazienti, generando nuove soluzioni se i pazienti incontrati risultano fuori posto
		for idPaziente in range(1, len(soluzioneA.pazienti) + 1):
			# Condizione in cui un paziente si trova in una posizione diversa rispetto le due soluzioni
			if soluzioneA.pazienti[idPaziente].ambulatorio != soluzioneB.pazienti[idPaziente].ambulatorio or soluzioneA.pazienti[idPaziente].posizione != soluzioneB.pazienti[idPaziente].posizione:
				nuovaSoluzione, nuovaMatrice = self.generaSoluzione(soluzioneA, idPaziente, soluzioneB)
				#print(nuovaSoluzione.livello," --- ",self.dive(nuovaMatrice, soluzioneB.generaMatricePosizione()))
				#input()
				posizioneStessaEnergia = self.ricercaDicotomica(listaSoluzioni, nuovaSoluzione.energia) # Ricerca posizione nella lista
				minPosizioneSoluzione, maxPosizioneSoluzione = self.trovaRangeStessaEnergia(listaSoluzioni, posizioneStessaEnergia) # Range soluzioni con identica energia
				
				if nuovaMatrice not in listaMatrici[minPosizioneSoluzione:maxPosizioneSoluzione + 1]: # Ricerca duplicati intelligente
					listaSoluzioni.insert(posizioneStessaEnergia, nuovaSoluzione)
					listaMatrici.insert(posizioneStessaEnergia, nuovaMatrice)
					
					# Limitazione lista delle soluzioni
					listaSoluzioni = listaSoluzioni[:self.config.dimensioneLista]
					listaMatrici = listaMatrici[:self.config.dimensioneLista]

				# Verifica riguardo alla bontà della nuova soluzione rispetto la migliore finora
				if nuovaSoluzione.energia < soluzioneMigliore.energia:
					soluzioneMigliore = nuovaSoluzione

		if soluzioneA.generaMatricePosizione() == soluzioneB.generaMatricePosizione():
			i+=1
			#print("i: ",i)
		return soluzioneMigliore, listaSoluzioni, listaMatrici,i

	def generaSoluzione(self, soluzioneA, idPaziente, soluzioneB):
		nuovaSoluzione = deepcopy(soluzioneA)
		
		pazienteA = nuovaSoluzione.pazienti[idPaziente] #Estrazione paziente dalla soluzione A
		pazienteB = soluzioneB.pazienti[idPaziente] #Estrazione paziente dalla soluzione B
		
		if len(nuovaSoluzione.ambulatori[pazienteB.ambulatorio]) <= pazienteB.posizione: # Il paziente occupa una posizione che non esiste nella soluzione B. Lo si aggiunge in coda
			startPazienteA = min(pazienteA.esami.values(), key=lambda x: x.valore).valore
			
			posizioneRealePaziente = self.spostaPaziente(pazienteA, pazienteB, nuovaSoluzione)
			
			if posizioneRealePaziente < 0: # Caso in cui il paziente precedente non esiste
				startMin = 0
			else: # Il paziente precedente esiste
				pazientePrecedente = nuovaSoluzione.ambulatori[pazienteB.ambulatorio][posizioneRealePaziente]
				tipoEsameMax, ultimoEsamePazientePrecedente = max(pazientePrecedente.esami.items(), key=lambda x: x[1].valore + getattr(self.config, "durata" + str(x[0])))
				finePazientePrecedente = ultimoEsamePazientePrecedente.valore + getattr(self.config, "durata" + str(tipoEsameMax))
				startMin = min(startPazienteA, finePazientePrecedente)
		else:
			# Questo controllo serve per identificare i buchi lasciate nelle liste a causa di pazienti mancanti (la posizione nella lista è diversa dalla posizione del paziente)
			if nuovaSoluzione.ambulatori[pazienteB.ambulatorio][pazienteB.posizione].posizione != pazienteB.posizione:
				startPazienteA = min(pazienteA.esami.values(), key=lambda x: x.valore).valore
				
				posizioneRealePaziente = self.spostaPaziente(pazienteA, pazienteB, nuovaSoluzione)
			
				if posizioneRealePaziente < 0: # Caso in cui il paziente precedente non esiste
					startMin = 0
				else: # Il paziente precedente esiste
					pazientePrecedente = nuovaSoluzione.ambulatori[pazienteB.ambulatorio][posizioneRealePaziente]
					tipoEsameMax, ultimoEsamePazientePrecedente = max(pazientePrecedente.esami.items(), key=lambda x: x[1].valore + getattr(self.config, "durata" + str(x[0])))
					finePazientePrecedente = ultimoEsamePazientePrecedente.valore + getattr(self.config, "durata" + str(tipoEsameMax))
					startMin = min(startPazienteA, finePazientePrecedente)
			else:
				# Scambio di pazienti con gli indici esistenti. Il paziente C è il paziente che viene scambiato con quello in esame (pazienteA)
				pazienteC = nuovaSoluzione.ambulatori[pazienteA.ambulatorio][pazienteA.posizione] = nuovaSoluzione.ambulatori[pazienteB.ambulatorio][pazienteB.posizione]
				nuovaSoluzione.ambulatori[pazienteB.ambulatorio][pazienteB.posizione] = pazienteA
				
				pazienteC.posizione = pazienteA.posizione
				pazienteC.ambulatorio = pazienteA.ambulatorio

				pazienteA.posizione = pazienteB.posizione
				pazienteA.ambulatorio = pazienteB.ambulatorio
				pazienteA.ordineEsami = pazienteB.ordineEsami

				startMin = min(list(pazienteA.esami.values()) + list(pazienteC.esami.values()), key=lambda x: x.valore).valore		

		# Operazioni per risolvere tutti i conflitti
		indiciPazienti = nuovaSoluzione.compattaAmbulatori(startMin)
		nuovaSoluzione.controlloConflitto(indiciPazienti)

		nuovaSoluzione.calcolaEnergia()
		# Creazione matrice per comparazione soluzioni
		matrice = nuovaSoluzione.generaMatricePosizione()
		
		pazienteA.pathRelinkingOsservato = True
		
		return nuovaSoluzione, matrice

	def spostaPaziente(self, pazienteA, pazienteB, soluzioneA):
		soluzioneA.ambulatori[pazienteA.ambulatorio].remove(pazienteA)
		
		# Aggiornamento posizione dei pazienti che venogno dopo il paziente eliminato (solo quelli che non sono stati ancora guardati)
		for paziente in soluzioneA.ambulatori[pazienteA.ambulatorio][pazienteA.posizione:]:
			if not paziente.pathRelinkingOsservato: # Le posizioni cambiano solo per i pazienti non osservati, in quanto le loro posizioni devono combaciare con la posizione attuale nell'ambulatorio della soluzione A
				paziente.posizione -= 1
				
		# Ricerca posizione corretta di inserimento
		indiceControllo = len(soluzioneA.ambulatori[pazienteB.ambulatorio]) - 1
		while indiceControllo >= 0 and soluzioneA.ambulatori[pazienteB.ambulatorio][indiceControllo].posizione > pazienteB.posizione:
			indiceControllo -= 1
		
		# Aggiornamento informazioni paziente (pazienteA ---> pazienteB)
		pazienteA.posizione = pazienteB.posizione
		pazienteA.ambulatorio = pazienteB.ambulatorio
		pazienteA.ordineEsami = pazienteB.ordineEsami

		# Inserimento paziente in ambulatorio
		soluzioneA.ambulatori[pazienteB.ambulatorio].insert(indiceControllo + 1, pazienteA)
		
		for paziente in soluzioneA.ambulatori[pazienteA.ambulatorio][indiceControllo + 2:]:
			if not paziente.pathRelinkingOsservato: # Le posizioni cambiano solo per i pazienti non osservati, in quanto le loro posizioni devono combaciare con la posizione attuale nell'ambulatorio della soluzione A
				paziente.posizione += 1
		
		return indiceControllo

	'''
	Ricerca della posizione per mantenere n migliori soluzioni. Il valore di ritorno è l'indice da utilizzare nell'operazione insert della lista
	di soluzioni.
	'''
	def ricercaDicotomica(self, listaSoluzioni, valore):
		posInizio = 0
		posFine = len(listaSoluzioni) - 1

		if posFine == -1: # Lista vuota
			return 0
		# Controllo sugli estremi della lista
		if valore <= listaSoluzioni[0].energia:
			return 0
		elif valore >= listaSoluzioni[-1].energia:
			return len(listaSoluzioni)
		else: # Ricerca
			while posInizio <= posFine:
				posMedia = floor((posInizio + posFine) / 2)
				
				if listaSoluzioni[posMedia].energia == valore: # Elemento trovato
					return posMedia
				elif listaSoluzioni[posMedia].energia > valore: # Ricerca sottolista a destra
					posInizio = posMedia + 1
				else: # Ricerca sottolista a sinistra
					posFine = posMedia - 1
			# A questo punto non è stata trovata nessuna soluzione salvata con la stessa energia. posInizio indica il punto per l'operazione insert 
			return posInizio

	'''
	Funzione che trova tute le soluzioni che possiedono la stessa energia dell'ultima generata e cercata precedentemente.
	Lo scopo è la riduzione di elementi che concorrono nella ricerca di soluzioni doppie.
	'''
	def trovaRangeStessaEnergia(self, listaSoluzioni, posizione):
		posMinima = posMassima = posizione
		
		while posMinima >= 1 and posMinima < len(listaSoluzioni):
			if listaSoluzioni[posMinima - 1].energia == listaSoluzioni[posMinima].energia:
				posMinima -= 1
			else:
				break
		while posMassima < len(listaSoluzioni) - 1:
			if listaSoluzioni[posMassima + 1].energia == listaSoluzioni[posMassima].energia:
				posMassima += 1
			else:
				break

		return posMinima, posMassima