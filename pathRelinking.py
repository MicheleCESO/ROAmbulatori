from euristica import *

class PathRelinking(SA):
	def __init__(self, config):
		self.config = config

	def start(self, soluzioneA, soluzioneB):
		soluzioniTrovate = []
		lunghezze = [len(soluzioneB[2][x]) - (soluzioneA[2][x]) for x in range(3)] # Indica il numero diverso di pazienti nei rispettivi ambulatori, visti dal punto di vista della soluzione A rispetto B
		
		pazientiA = soluzioneA[0]
		ambulatoriA = soluzioneA[2]
		pzientiB = soluzioneB[0]
		ambulatoriB = soluzioneB[2]
		
		for idPaziente in range(1, len(pazientiA) + 1):
			posizioneA = ambulatoriA[pazientiA[idPaziente]["ambulatorio"]].index(pazientiA[idPaziente])
			posizioneB = ambulatoriB[pazientiB[idPaziente]["ambulatorio"]].index(pazientiB[idPaziente])
			if pazientiA[idPaziente]["ambulatorio"] != pazientiB[idPaziente]["ambulatorio"] or posizioneA != posizioneB: # Condizione in cui un paziente si trova in una posizione diversa
				nuovaSoluzione = self.generaSoluzione()
				soluzioniTrovate.append(nuovaSoluzione)
				