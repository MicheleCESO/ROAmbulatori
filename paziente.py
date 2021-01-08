class Paziente():
	def __init__(self):
		self.id = None
		self.esami = {}
		self.ordineEsami = []
		self.ambulatorio = None
		self.durataTotale = None
		self.posizione = None
		self.pathRelinkingOsservato = False