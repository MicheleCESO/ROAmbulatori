import configparser

conf=None
# Funzione per generare un file di configurazione nel caso manchi.
def genConfig():
	config = configparser.ConfigParser()
	config.optionxform = str	# Per ottenere case sensitive senza alterare altro oltre alla funzione qui riportata

	dicti = {
				"Parametri":
				{	"PesoConflitto"	:	1,
					"PesoMakespan"	:	1,
					"Temperatura"	:	2000,
					"Iterazioni"	:	5000
				},

				"Istanze":
				{
					"MinPazienti"	:	10,
					"MaxPazienti"	:	20,
					"MinTasks"		:	1,
					"MaxTasks"		:	5
				}
			}
	# Popolamento della struttura dati per generare il file di configurazione
	for section, values in dicti.items():
		config[section] = values

	# Scrittura del file
	with open("config.ini","w") as configfile:
		config.write(configfile)
	conf = dicti
	return dicti

# Funzione per caricare un file di configurazione.
def loadConfig():
	config = configparser.ConfigParser()
	config.optionxform = str

	# Lettura del file di configurazione
	config.read("config.ini")

	# Popolamento del dizionario da tenere in memoria
	dicti = {}
	for sect in config.sections():
		dicti[sect] = {}
		for key in config[sect]:
			dicti[sect][key] = int(config[sect][key])
	return dicti

# Funzione per mostrare la configurazione in uso
def showConfig(conf):
	for section, params in conf.items():
		print("\n[{}]\n".format(section))
		for key,value in params.items():
			print(key,"=",value)
	input("\nPremi per continuare...")

# Funzione per alterare la configurazione in uso e salvata nel file
def changeConfig(conf):
	flag = True
	while flag:
		print("Quale parametro modificare?")
		i = 1		# Indice delle voci
		dicti = {}	# Dizionario di appoggio
		for section, params in conf.items():
			print("\n[{}]\n".format(section))
			for key,value in params.items():
				print("{}) {}: [{}]".format(i,key,value))
				dicti[i] = [section,key]
				i += 1
		print("{}) Indietro".format(i))
		try:
			scelta = int(input("\n"))
			flag = False
		except ValueError:
			print("\nInput errato.\n")
	if scelta in range(1,i):
		try:
			valore = int(input("\nInserisci il nuovo valore per {} (premi 0 per annullare): ".format(dicti[scelta][1])))
		except ValueError:
			print("\nInput errato, configurazione non modificata.\n")
			return
		if valore == 0:
			print("\nAnnullato.\n")
			return
		conf[dicti[scelta][0]][dicti[scelta][1]] = valore # Aggiorno il valore di configurazione

		# Salvataggio su file
		config = configparser.ConfigParser()
		config.optionxform = str

		# Popolamento della struttura dati per generare il file di configurazione
		for section, values in conf.items():
			print(section,values)
			config[section] = values

		with open("config.ini","w") as configfile:
			config.write(configfile)
	elif scelta == i: # L'utente torna indietro
		pass
	else:
		print("\nScelta inesistente. Configurazione non modificata\n")

if __name__ == "__main__":
	a = genConfig()
	a = loadConfig()
	print(a)
	showConfig(a)
	changeConfig(a)