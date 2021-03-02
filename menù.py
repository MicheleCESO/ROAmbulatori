from istanza import Istanza
from greedy import Greedy
from simulatedAnnealing import SimulatedAnnealing
from pathRelinking import PathRelinking
import os
from heapq import nsmallest
from random import choice

class Menù():
	def __init__(self, config, mainW):
		self.config = config # Configurazione
		self.mainW = mainW	 # Interfaccia grafica
		
		# Istanze degli algoritmi
		self.classeIstanza = Istanza(config)
		self.classeGreedy = Greedy(config)
		self.classeSimulatedAnnealing = SimulatedAnnealing(config)
		self.classePathRelinking = PathRelinking(config)
		
		# Strutture dati contenenti i contenitori per la grafica
		self.graficaGreedy = [mainW.greedy_1, mainW.greedy_2]
		self.graficaSA = [mainW.simulated_annealing_1, mainW.simulated_annealing_2]
		self.graficaPR = [mainW.path_relinking_1, mainW.path_relinking_2]
		
		# Struttura dati contenente le soluzioni create
		self.istanzaCorrente = None
		self.listaGreedy = []
		self.listaSimulatedAnnealing = []
		self.listaPathRelinking = []
	
	'''
	Funzione eseguita dal thread demone, gestisce l'interfaccia utente.
	'''
	def start(self):
		# Menù contestuale

		titolo = """
                 ______                            _    _                _  _                                     
                 | ___ \                          | |  | |              | |(_)                                    
                 | |_/ / _ __   ___    __ _   ___ | |_ | |_   ___     __| | _                                     
                 |  __/ | '__| / _ \  / _` | / _ \| __|| __| / _ \   / _` || |                                    
                 | |    | |   | (_) || (_| ||  __/| |_ | |_ | (_) | | (_| || |                                    
                 \_|    |_|    \___/  \__, | \___| \__| \__| \___/   \__,_||_|                                    
                                       __/ |                                                                      
                                      |___/                                                                       
______  _                                  _____                            _    _               
| ___ \(_)                                |  _  |                          | |  (_)              
| |_/ / _   ___   ___  _ __   ___   __ _  | | | | _ __    ___  _ __   __ _ | |_  _ __   __  __ _ 
|    / | | / __| / _ \| '__| / __| / _` | | | | || '_ \  / _ \| '__| / _` || __|| |\ \ / / / _` |
| |\ \ | || (__ |  __/| |   | (__ | (_| | \ \_/ /| |_) ||  __/| |   | (_| || |_ | | \ V / | (_| |
\_| \_||_| \___| \___||_|    \___| \__,_|  \___/ | .__/  \___||_|    \__,_| \__||_|  \_/   \__,_|
                                                 | |                                             
                                                 |_|                                             """
		print(titolo)

		# Dizionario per gestire la scelta utente
		scelta = {
					1 : self.soluzioneAutomatica,
					2 : self.nuovaIstanza,
					3 : self.nuovaGreedy,
					4 : self.nuovoSA,
					5 : self.nuovoPR,
					6 : self.visualizzaMigliori,
					7 : self.visualizzaMigliore,
					8 : self.config.mostra,
					9 : self.config.modifica,
					10 : self.aiuto,
					11 : self.uscita
		}
		
		# Menù principale
		while True:
			try:
				risposta = int(input(
"""\nSelezionare un'opzione:

1) Crea soluzione automatica (istanza + GRASP + PR)
2) Crea una nuova istanza
3) Applica un algoritmo Greedy
4) Applica Simulated Annealing
5) Applica Path Relinking
6) Visualizza dati soluzioni migliori per categoria
7) Visualizza soluzione migliore
8) Visualizza configurazione
9) Modifica configurazione
10) Aiuto
11) Esci

>: """))
				if risposta < 1 or risposta > len(scelta):
					raise ValueError()
			except ValueError:
				print("\nInput errato.")
			else:
				scelta[risposta]()
	
	'''
	Funzione per generare una soluzione ottima utilizzando il metodo GRASP + Path Relinking, tutto automatizzato.
	'''
	def soluzioneAutomatica(self):
		print("\nGenerazione nuova istanza...\n")
		self.nuovaIstanza()
		print("Generazione istanza completata.\n\n Inizio generazione soluzioni greedy...\n")

		# Greedy
		tipoGreedy = ["LPT", "SPT", "FIFO"]
		for i in range(self.config.GreedyGenerabili):
			print("Generazione soluzione {} di {}\n".format(i + 1, self.config.GreedyGenerabili))
			self.listaGreedy.append(self.classeGreedy.start(self.istanzaCorrente, choice(tipoGreedy)))
		print("Generazione soluzioni greedy completata.\n")
		# Simulated Annealing
		print("Inizio generazione soluzioni Simulated Annealing...\n")
		for i, greedy in enumerate(self.listaGreedy, start=1):
			print("Generazione soluzione {} di {}\n".format(i, len(self.listaGreedy)))
			self.listaSimulatedAnnealing.append(self.classeSimulatedAnnealing.start(greedy))
		print("Generazione soluzioni Simulated Annealing completata.\n")
		
		# Path Relinking
		print("Inizio generazione soluzioni Path Relinking...\n")
		for i in range(self.config.PRGenerabili):
			print("Generazione soluzione {} di {}\n".format(i + 1, self.config.PRGenerabili))
			self.listaPathRelinking.append(self.classePathRelinking.start(choice(self.listaSimulatedAnnealing), choice(self.listaSimulatedAnnealing)))
		print("Generazione soluzioni Path Relinking completata.")
		
		# Ricerca soluzione migliore
		soluzioniTotali = self.listaGreedy + self.listaSimulatedAnnealing + self.listaPathRelinking
		soluzioneMigliore = nsmallest(1, soluzioniTotali, key=lambda x : x.makeSpan)[0]

		if soluzioneMigliore.tipo == "G":
			self.graficaGreedy[0].tipo = soluzioneMigliore.tipoGreedy
			self.graficaGreedy[0].popolamentoDati(soluzioneMigliore)
		elif soluzioneMigliore.tipo == "SA":
			self.graficaSA[0].popolamentoDati(soluzioneMigliore)
		else:
			self.graficaPR[0].popolamentoDati(soluzioneMigliore)
		
		self.visualizzaSoluzione(soluzioneMigliore)

	'''
	Funzione per creare una nuova istanza del problema e graficarla.
	'''
	def nuovaIstanza(self):
		self.istanzaCorrente = self.classeIstanza.start()

		# Reset completo di grafica e soluzioni
		self.resetGrafica()
		self.listaGreedy = []
		self.listaSimulatedAnnealing = []
		self.listaPathRelinking = []

		self.mainW.istanza.popolamentoDati(self.istanzaCorrente)
	
	'''
	Funzione per creare una nuova soluzione greedy. Viene richiesto all'utente la tipologia desiderata di greedy, infine viene graficata la soluzione creata.
	'''
	def nuovaGreedy(self):
		if not self.istanzaCorrente:
			print("\nUna soluzione greedy necessita di una istanza di un problema per poter operare.\nPrima di creare nuove soluzioni, generare una nuova istanza.\n")
			input(">: Premere un tasto per continuare")
			return
		
		# Dizionario per gestire la scelta utente
		scelta = {
					1 : "LPT",
					2 : "SPT",
					3 : "FIFO",
		}
		
		# Richiesta tipologia greedy iterativa
		flag = True
		while flag:
			flag = False
			risposta = input(
"""\nQuale tipologia greedy utilizzare? (premere Invio per annullare):

1) LPT (Longest Processing Time)
2) SPT (Shortest Processing Time)
3) FIFO (First In First Out)

>: """)
			if risposta == "":
				print("\nAnnullato")
				return
			try:
				risposta = int(risposta)
				if risposta < 1 or risposta > len(scelta):
					raise ValueError()
			except ValueError:
				print("\nInput errato.\n\n")
				flag = True
			else:
				# Nuova soluzione
				nuovaGreedy = self.classeGreedy.start(self.istanzaCorrente, scelta[risposta])
				
				# Visualizzazione e salvataggio in memoria
				self.listaGreedy.append(nuovaGreedy)
				self.resetGrafica()
				self.graficaGreedy[0].tipo = scelta[risposta] 
				self.graficaGreedy[0].popolamentoDati(nuovaGreedy)
				
				self.visualizzaSoluzione(nuovaGreedy)

	'''
	Funzione che genera una nuova soluzione SA a partire da una soluzione greedy. La soluzione viene infine graficata.
	'''
	def nuovoSA(self):
		if len(self.listaGreedy) + len(self.listaSimulatedAnnealing) + len(self.listaPathRelinking) == 0:
			print("\nSimulated Annealing necessita di una soluzione iniziale.\nPrima di utilizzare questo algoritmo, generare una nuova soluzione di classe Greedy.\n")
			input(">: Premere un tasto per continuare")
			return
		
		flag = True
		while flag:
			flag = False
			print("\nQuale soluzione adottare?")
			indice = 1
			if len(self.listaGreedy) > 0:
				print("\n[Soluzioni Greedy]\n")
				for soluzione in self.listaGreedy:
					print(str(indice) + ") Tipo: " + soluzione.tipoGreedy + " Energia: " + str(soluzione.energia) + " Efficienza: " + "{:.2%}".format(soluzione.efficienza) + " Makespan: " + str(soluzione.makeSpan))
					indice += 1
			if len(self.listaSimulatedAnnealing) > 0:
				print("\n[Soluzioni Simulated Annealing]\n")
				for soluzione in self.listaSimulatedAnnealing:
					print(str(indice) + ") Energia: " + str(soluzione.energia) + " Efficienza: " + "{:.2%}".format(soluzione.efficienza) + " Makespan: " + str(soluzione.makeSpan))
					indice += 1
			if len(self.listaPathRelinking) > 0:
				print("\n[Soluzioni Path Relinking]\n")
				for soluzione in self.listaPathRelinking:
					print(str(indice) + ") Energia: " + str(soluzione.energia) + " Efficienza: " + "{:.2%}".format(soluzione.efficienza) + " Makespan: " + str(soluzione.makeSpan))
					indice += 1
			
			# Input utente
			risposta = input("\n(premere Invio per annullare)>: ")
			if risposta == "":
				print("\nAnnullato")
				return
			try:
				risposta = int(risposta)
				if risposta < 1 or risposta > indice - 1:
					raise ValueError()
			except ValueError:
				print("\nInput errato.")
				flag = True
			else:
				# Nuova soluzione
				listaTotale = self.listaGreedy + self.listaSimulatedAnnealing + self.listaPathRelinking
				soluzione = listaTotale[risposta - 1]
				nuovoSA = self.classeSimulatedAnnealing.start(soluzione)
				
				self.confrontaSoluzioni(nuovoSA, soluzione)
				
				# Visualizzazione e salvataggio in memoria
				self.listaSimulatedAnnealing.append(nuovoSA)
				self.resetGrafica()
				self.graficaSA[0].popolamentoDati(nuovoSA)

				# Visualizzazione soluzione di partenza
				if soluzione.tipo == "G":
					self.graficaGreedy[0].tipo = soluzione.tipoGreedy
					self.graficaGreedy[0].popolamentoDati(soluzione)
				elif soluzione.tipo == "SA":
					self.graficaSA[1].popolamentoDati(soluzione)
				else:
					self.graficaPR[0].popolamentoDati(soluzione)
	
	'''
	Funzione che crea una soluzione Path Relinking partendo da due soluzioni iniziali, definite dall'utente, perciò di qualsiasi classe.
	'''
	def nuovoPR(self):
		if len(self.listaGreedy) + len(self.listaSimulatedAnnealing) < 2:
			print("\nPath Relinking necessita di due soluzioni iniziali.\nPrima di utilizzare questo algoritmo, generare due nuove soluzioni di classe Greedy o Simulated Annealing.\n")
			input(">: Premere un tasto per continuare")
			return
		
		soluzioniScelte = []
		flag = True
		while flag:
			flag = False
			print("\nQuale soluzione adottare?")
			indice = 1
			if len(self.listaGreedy) > 0:
				print("\n[Soluzioni Greedy]\n")
				for soluzione in self.listaGreedy:
					print(str(indice) + ") Tipo: " + soluzione.tipoGreedy + " Energia: " + str(soluzione.energia) + " Efficienza: " + "{:.2%}".format(soluzione.efficienza) + " Makespan: " + str(soluzione.makeSpan))
					indice += 1
			if len(self.listaSimulatedAnnealing) > 0:
				print("\n[Soluzioni Simulated Annealing]\n")
				for soluzione in self.listaSimulatedAnnealing:
					print(str(indice) + ") Energia: " + str(soluzione.energia) + " Efficienza: " + "{:.2%}".format(soluzione.efficienza) + " Makespan: " + str(soluzione.makeSpan))
					indice += 1
			if len(self.listaPathRelinking) > 0:
				print("\n[Soluzioni Path Relinking]\n")
				for soluzione in self.listaPathRelinking:
					print(str(indice) + ") Energia: " + str(soluzione.energia) + " Efficienza: " + "{:.2%}".format(soluzione.efficienza) + " Makespan: " + str(soluzione.makeSpan))
					indice += 1
			
			# Input utente
			risposta = input("\n(premere Invio per annullare)>: ")
			if risposta == "":
				print("\nAnnullato")
			try:
				risposta = int(risposta)
				if risposta < 1 or risposta > indice - 1:
					raise ValueError()
			except ValueError:
				print("\nInput errato.")
				flag = True
			else:
				# Nuova soluzione
				listaTotale = self.listaGreedy + self.listaSimulatedAnnealing + self.listaPathRelinking
				soluzioniScelte.append(listaTotale[risposta - 1])
				if len(soluzioniScelte) < 2: # Se non sono state scelte due soluzioni, ne verrà richiesta un'altra
					flag = True
		
		# Avvio algoritmo Path Relinking
		nuovoPR = self.classePathRelinking.start(soluzioniScelte[0], soluzioniScelte[1])
	
		# Visualizzazione e salvataggio in memoria
		self.listaPathRelinking.append(nuovoPR)
		self.resetGrafica()
		self.graficaPR[0].popolamentoDati(nuovoPR)

		# Stampa delle informazioni delle soluzioni
		self.confrontaSoluzioni(nuovoPR, soluzioniScelte[0], soluzioniScelte[1])
		
		# Visualizzazione soluzioni iniziali
		indiceG = 0
		indiceSA = 0
		indicePR = 1
		for soluzione in soluzioniScelte:
			if soluzione.tipo == "G":
				self.graficaGreedy[indiceG].tipo = soluzione.tipoGreedy
				self.graficaGreedy[indiceG].popolamentoDati(soluzione)
				indiceG += 1
			elif soluzione.tipo == "SA":
				self.graficaSA[indiceSA].popolamentoDati(soluzione)
				indiceSA += 1
			else:
				self.graficaPR[indicePR].popolamentoDati(soluzione)
				indicePR += 1

	'''
	Funzione che mostra le soluzioni migliori ottenute attualmente per ogni classe di algoritmi.
	'''
	def visualizzaMigliori(self):
		# Ricerca heap per visualizzare le soluzioni migliori
		solG = nsmallest(2, self.listaGreedy, key= lambda x : x.makeSpan)
		solSA = nsmallest(2, self.listaSimulatedAnnealing, key= lambda x : x.makeSpan)
		solPR = nsmallest(2, self.listaPathRelinking, key= lambda x : x.makeSpan)
		
		self.resetGrafica()
		
		indiceG = 0
		indiceSA = 0
		indicePR = 0
		for soluzione in solG:
			self.visualizzaSoluzione(soluzione)
			self.graficaGreedy[indiceG].popolamentoDati(soluzione)
			self.graficaGreedy[indiceG].tipo = soluzione.tipoGreedy
			indiceG += 1
		for soluzione in solSA:
			self.visualizzaSoluzione(soluzione)
			self.graficaSA[indiceSA].popolamentoDati(soluzione)
			indiceSA += 1
		for soluzione in solPR:
			self.visualizzaSoluzione(soluzione)
			self.graficaPR[indicePR].popolamentoDati(soluzione)
			indicePR += 1
	
	'''
	Funzione per visualizzare la soluzione migliore trovata finora.
	'''
	def visualizzaMigliore(self):
		listaCompleta = self.listaGreedy + self.listaSimulatedAnnealing + self.listaPathRelinking
		soluzione = nsmallest(1, listaCompleta, key=lambda x : x.makeSpan)[0]
		
		self.visualizzaSoluzione(soluzione)

		# Per la grafica
		self.resetGrafica()
		
		if soluzione.tipo == "G":
			self.graficaGreedy[0].popolamentoDati(soluzione)
		elif soluzione.tipo == "SA":
			self.graficaSA[0].popolamentoDati(soluzione)
		else:
			self.graficaPR[0].popolamentoDati(soluzione)
	
	'''
	Funzione per cancellare tutte le visualizzazioni degli algoritmi.
	'''
	def resetGrafica(self):
		for grafico in self.graficaGreedy + self.graficaSA + self.graficaPR:
			grafico.cancellaDati()
	
	'''
	Funzione per la schermata informativa.
	'''
	def aiuto(self):
		print("""
Premessa:

Il programma gestisce il seguente problema:

Lo scenario si compone di un poliambulatorio, composto da tre ambulatori medici identici e cinque medici, ognuno specializzato in un esame medico diverso. In tutto, gli ambulatori possono fornire un totale di cinque esami diversi.
Nel poliambulatorio entrano alcuni pazienti (numero variabile), ognuno può scegliere a quali esami sottoporsi, da  un minimo di uno, ad un massimo di cinque. Quando un paziente occupa un ambulatorio, deve rimanerci dentro fino alla completa risoluzione di tutti i suoi esami, inoltre egli preclude ad altri la possibilità di utilizzare l'ambulatorio occupato.
Siccome ogni tipologia di esame può essere eseguita solo da un medico in particolare, nello stesso istante non possono essere in esecuzione esami della stessa natura in ambulatori diversi.
L'obiettivo del problema è fornire tutte le prestazioni mediche richiete dai pazienti, avendo un makespan minimo.

Caratteristiche:

Il programma permette all'utente di creare un nuovo problema da risolvere, partendo da una configurazione estesa personalizzabile.
Successivamente è possibile creare soluzioni utilizzando diversi algoritmi:

- Greedy: soluzione di partenza in cui è possibile sceglierne la tipologia (LPT, SPT, FIFO) e se utilizzare la randomicità durante la creazione.
- Simulated Annealing: ricerca locale utilizzata per migliorare una soluzione.
- Path Relinking: ricerca nello spazio ristretto alle soluzioni simili a quelle di input della procedura

All'utente viene fornita la possibilità di gestire manualmente la creazione delle soluzioni, oppure di avvalersi di una procedura automatica che, partendo dalla creazione di una nuova istanza del problema e arrivando all'applicazione di Path Relinking, genera una soluzione ottima al problema attuale.
L'interfaccia grafica prevede una semplice visualizzazione delle soluzioni generate, utile per il confronto manuale da parte dell'utente.
		""")
		input(">: Premere un tasto per continuare")
	
	'''
	Funzione per visualizzare informazioni inerenti la soluzione ottenuta.
	'''
	def visualizzaSoluzione(self, soluzione):
		print("\nTipologia soluzione: {}\nMakespan: {}\nEfficienza: {:.2%}".format(soluzione.tipo, soluzione.makeSpan, soluzione.efficienza))
	
	'''
	Funzione che mostra eventuali migliorie ottenute con la nuova soluzione. nuovaSoluzione2 è la seconda soluzione utilizzata durante Path Relinking.
	'''
	def confrontaSoluzioni(self, nuovaSoluzione, vecchiaSoluzione, vecchiaSoluzione2=None):
		print("\nNuova soluzione:")
		self.visualizzaSoluzione(nuovaSoluzione)
		print("------------------")
		
		self.visualizzaSoluzione(vecchiaSoluzione)
		if vecchiaSoluzione2:
			self.visualizzaSoluzione(vecchiaSoluzione2)
			vecchiaSoluzioneMin = min([vecchiaSoluzione, vecchiaSoluzione2], key=lambda x : x.makeSpan)
		else:
			vecchiaSoluzioneMin = vecchiaSoluzione
		print("\nRisultato finale:")
		percentualeFinale = nuovaSoluzione.makeSpan / vecchiaSoluzioneMin.makeSpan
		
		if percentualeFinale > 1:
			print("\nLa nuova soluzione è peggiorata del {:.2%}.".format(1 - percentualeFinale))
		elif percentualeFinale == 1:
			print("\nLa nuova soluzione possiede lo stesso makespan.\n")
		else:
			print("\nLa nuova soluzione è migliorata del {:.2%}.".format(1 - percentualeFinale))
	'''
	Funzione per la gestione dell'uscita dal thread e dal programma.
	'''
	def uscita(self):
		os._exit(1)