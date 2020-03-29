from configparser import ConfigParser
from time import sleep

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
						"minPazienti"	:	[10,	int],
						"maxPazienti"	:	[20,	int],
						"p1Esami"		:	[20,	int, float],
						"p2Esami"		:	[20,	int, float],
						"p3Esami"		:	[20,	int, float],
						"p4Esami"		:	[20,	int, float],
						"p5Esami"		:	[20,	int, float],
						"pEsame1"		:	[20,	int, float],
						"pEsame2"		:	[20,	int, float],
						"pEsame3"		:	[20,	int, float],
						"pEsame4"		:	[20,	int, float],
						"pEsame5"		:	[20,	int, float]
					},
					
					"Parametri":
					{	"temperatura"			:	[2000,	int, float],
						"tassoRaffreddamento"	:	[0.99,		float],
						"iterazioni"			:	[10000,		int]
					}

				}
		
		if isfile("config.ini"):
			self.carica()
		else:
			self.genera()

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

	def carica(self):
		config = ConfigParser()
		config.optionxform = str

		# Lettura del file di configurazione
		config.read("config.ini")
		
		self.validazioneTotale(config)

	def validazioneTotale(self, config):
		for sezione, valori in self.schema.items():
			if sezione not in config:
				raise SectionError("Sezione '%s' mancante nel file di configurazione." % sezione)
			for chiave, valore in valori.items():
				if chiave not in config[sezione] or config[sezione][chiave] == '':
					raise MissingError("Parametro '%s' mancante nella sezione '%s' del file di configurazione." % (chiave, sezione))
				try:
					parametro = eval(config[sezione][chiave])
				except NameError as e:
					print("NameError: Errore valore parametro '%s', sezione '%s' del file di configurazione." % (chiave, sezione))
				if type(parametro) not in valore:
					raise ValueError("Valore del parametro '%s' errato nella sezione '%s'. Tipo previsto: %s." % (chiave, sezione, str(valore[1:])))
				else:
					setattr(self, chiave, parametro)
	
	def validazioneParametro(self, parametri):
		for chiave, valore in parametri.items():
			try:
				parametro = eval(valore)
			except NameError as e:
				print("NameError: Errore valore parametro '%s', sezione '%s' del file di configurazione." % (chiave, sezione))
			lista = list(self.schema.keys())
			flag = True
			while lista and flag:
				sezione = lista.pop()
				if chiave in self.schema[sezione]:
					flag = False
			if type(parametro) not in self.schema[sezione][chiave][1:]: # Controllo tipologia nuovo valore con i tipi possibili descritti
				 print("Valore del parametro '%s' errato nella sezione '%s'. Tipo previsto: %s." % (chiave, sezione, valore[1]))
			else:
				setattr(self, chiave, parametro)

class NoGuiConfig(Config):
	def __init__(self):
		super().__init__()
				
	# Funzione per mostrare la configurazione in uso
	def mostra(self):
		for sezione, parametri in self.schema.items():
			print("[%s]\n" % sezione)
			for chiave in parametri:
				print(chiave,"=",getattr(self, chiave))
			print("")
				
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
					dicti[i] = [sezione, chiave]
					i += 1
			print("%s) Indietro" % i)
			try:
				scelta = int(input("\n"))
				flag = False
			except ValueError:
				print("\nInput errato.\n")
				sleep(2)
		if scelta in range(1,i):
			try:
				valore = int(input("\nInserisci il nuovo valore per %s (premi 0 per annullare): " % dicti[scelta][1]))
			except ValueError:
				print("\nInput errato, configurazione non modificata.")
				sleep(2)
				return
			if valore == 0:
				print("\nAnnullato.")
				sleep(2)
				return
			setattr(self, chiave, valore) # Aggiorno il valore di configurazione

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

if __name__ == "__main__":
	c = Config()