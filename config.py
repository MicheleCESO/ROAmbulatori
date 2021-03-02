from configparser import ConfigParser

class SectionError(Exception): # Eccezione mancanza di sezione
	pass

class MissingError(Exception): # Eccezione mancanza di parametri
	pass
	
class Config():
	def __init__(self):
		from os.path import isfile
		
		# Dizionario dei parametri che il modulo configparser necessita per creare il file di configurazione
		self.schema = {
					"Istanze":
					{
						"minPazienti"			:	[10,		int],
						"maxPazienti"			:	[20,		int],
						"p1Esami"				:	[20.0,		float],
						"p2Esami"				:	[20.0,		float],
						"p3Esami"				:	[20.0,		float],
						"p4Esami"				:	[20.0,		float],
						"p5Esami"				:	[20.0,		float],
						"pEsame1"				:	[20.0,		float],
						"pEsame2"				:	[20.0,		float],
						"pEsame3"				:	[20.0,		float],
						"pEsame4"				:	[20.0,		float],
						"pEsame5"				:	[20.0,		float],
						"durata1"				:	[1,			int],
						"durata2"				:	[2,			int],
						"durata3"				:	[3,			int],
						"durata4"				:	[4,			int],
						"durata5"				:	[5,			int],
						"GreedyGenerabili"		:	[50,		int],
						"PRGenerabili"			:	[50,		int]
					},
					
					"SA":
					{	"temperatura"			:	[2000.0,	float],
						"tassoRaffreddamento"	:	[0.99,		float],
						"sogliaCaloreMinimo"	:	[0.0002,	float],
						"probabilitàScambio"	:	[0.5,		float]
					},

					"Path Relinking":
					{	"dimensioneLista"		:	[1,			int],
						"percorsiDaCompletare"	:	[5000,		int]
					}

				}

		if isfile("config.ini"):
			self.carica()
		else:
			self.genera()

	'''
	Funzione per generare un nuovo file di configurazione. Viene utilizzato lo schema salvato nella classe come punto di riferimento.
	'''
	def genera(self):
		config = ConfigParser()
		config.optionxform = str # Per ottenere case sensitive senza alterare altro oltre alla funzione qui riportata

		# Popolamento della struttura dati per generare il file di configurazione
		for sezione, valori in self.schema.items():
			config[sezione] = {} # Crea una sezione con i propri valori
			for chiave, valore in valori.items():
				config[sezione][chiave] = str(valore[0])
				setattr(self, chiave, valore[0]) # Creo un attributo della classe

		# Scrittura del file
		with open("config.ini","w") as configFile:
			config.write(configFile)
	
	'''
	Funzione per caricare una configurazione da file.
	'''
	def carica(self):
		config = ConfigParser()
		config.optionxform = str

		# Lettura del file di configurazione
		config.read("config.ini")
		
		self.validazioneTotale(config)

	'''
	Funzione per salvare la configurazione corrente su file, in modo da renderla permanente.
	'''
	def salva(self):
		config = ConfigParser()
		config.optionxform = str # Per ottenere case sensitive senza alterare altro oltre alla funzione qui riportata

		# Popolamento della struttura dati per generare il file di configurazione
		for sezione, valori in self.schema.items():
			config[sezione] = {} # Crea una sezione con i propri valori
			for chiave, valore in valori.items():
				config[sezione][chiave] = str(getattr(self, chiave))

		# Scrittura del file
		with open("config.ini","w") as configFile:
			config.write(configFile)
	
	'''
	Funzione per validare un file di configurazione.
	'''
	def validazioneTotale(self, config):
		for sezione, parametri in self.schema.items():
			if sezione not in config:
				raise SectionError("Sezione '%s' mancante nel file di configurazione." % sezione)
			for chiave, valore in parametri.items():
				if chiave not in config[sezione] or config[sezione][chiave] == '':
					raise MissingError("Parametro '%s' mancante nella sezione '%s' del file di configurazione." % (chiave, sezione))
				try:
					parametro = valore[1](config[sezione][chiave]) # Conversione da stringa a tipologia definita dallo schema
				except ValueError:
					print("Errore valore parametro '%s', sezione '%s' del file di configurazione." % (chiave, sezione))
				else:
					setattr(self, chiave, parametro)
	
	'''
	Funzione per visualizzare la configurazione utilizzata.
	'''
	def mostra(self):
		for sezione, parametri in self.schema.items():
			print("[%s]\n" % sezione)
			for chiave in parametri:
				print(chiave,"=",getattr(self, chiave))
			print("")
	
	'''
	Funzione che permette l'alterazione della configurazione. Viene richiesto all'utente quale parametro modificare, successivamente viene richiesto il nuovo valore.
	'''
	def modifica(self):
		flag = True
		while flag:
			print("Quale parametro modificare?")
			i = 1		# Indice delle voci
			dicti = {}	# Dizionario di appoggio
			for sezione, parametri in self.schema.items():
				print("\n[%s]\n" % sezione)
				for chiave, valore in parametri.items():
					print("%s) %s: [%s]" % (i, chiave, getattr(self, chiave)))
					dicti[i] = [sezione, chiave, getattr(self, chiave), valore[1]] # Composizione: sezione, chiave, valore, tipo di dato
					i += 1
			
			# Scelta utente
			scelta = input("\n(premere Invio per annullare)>: ")
			if scelta == "":
				print("\nAnnullato")
				return
			try:
				scelta = int(scelta)
				if scelta > i - 1 or scelta < 0:
					raise ValueError()
			except ValueError:
				print("\nInput errato.\n")
			else:
				flag = False
		
		# Scelta accettata, richiesto nuovo valore
		if scelta in range(1,i):
			valore = input("\nInserisci il nuovo valore per %s [%s] (premi Invio per annullare)>: " % (dicti[scelta][1], dicti[scelta][2]))
			if valore == "":
				print("\nAnnullato.")
				return
			else:
				try:
					valore = dicti[scelta][3](valore) # Conversione tipo indicato dallo schema
					if valore < 0:
						raise ValueError()
				except ValueError:
					print("\nInput errato, configurazione non modificata.")
					return

			setattr(self, dicti[scelta][1], valore) # Aggiorno il valore di configurazione

			# Salvataggio su file
			config = ConfigParser()
			config.optionxform = str

			for sezione, valori in self.schema.items():
				config[sezione] = {} # Crea una sezione con i propri valori
				for chiave, valore in valori.items():
					config[sezione][chiave] = str(getattr(self, chiave))

			with open("config.ini","w") as configfile:
				config.write(configfile)
		elif scelta == i: # L'utente torna indietro
			print("")
		else:
			print("\nScelta inesistente. Configurazione non modificata\n")