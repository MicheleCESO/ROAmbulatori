from PyQt5 import QtWidgets, uic, QtGui, QtCore
import pyqtgraph as pg
import sys
from time import sleep

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, conf):
		super(MainWindow, self).__init__()
		self.config = conf # Configurazione
		uic.loadUi("GUI3.ui", self)

		# Passaggio parametri a widget
		self.istanza.inizializzaPar(conf, "Istanza")
		self.greedy_1.inizializzaPar(conf, "Greedy slot 1")
		self.greedy_2.inizializzaPar(conf, "Greedy slot 2")
		self.simulated_annealing_1.inizializzaPar(conf, "Simulated Annealing slot 1")
		self.simulated_annealing_2.inizializzaPar(conf, "Simulated Annealing slot 2")
		self.path_relinking_1.inizializzaPar(conf, "Path Relinking slot 1")
		self.path_relinking_2.inizializzaPar(conf, "Path Relinking slot 2")

class Widget(QtGui.QWidget):		
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tipo = ""
		self.rettangoli = []
		self.labels = []
		self.linee = []
		self.valoriUsati = []
		self.posIniziale = 0
		self.posFinale = 0
		self.val = 0
		self.offsetWindow = 0
		self.colori = 	[
							QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.SolidPattern),
							QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern),
							QtGui.QBrush(QtCore.Qt.cyan, QtCore.Qt.SolidPattern),
							QtGui.QBrush(QtCore.Qt.yellow, QtCore.Qt.SolidPattern),
							QtGui.QBrush(QtCore.Qt.magenta, QtCore.Qt.SolidPattern)
						]
		
		# Palette background
		self.pal = self.palette()
		self.pal.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
		
	def inizializzaPar(self, conf, nome):
		self.config = conf
		self.nome = nome

		self.scala = 50	# Scala dell'intero grafico
		self.altezza = 30 # Altezza dei rettangoli
		self.offsetx = 50 # Distanza dalla coordinata 0
		self.offsety = 20 # Distanza dalla coordinata 0 
		self.offsetLabely = 10 # Distanza tra asse X e labels
		self.compAssey = self.altezza * 3 + self.offsety # Altezza dell'origine O

	'''
	Funzione che cancella tutte le parti grafiche
	'''
	def cancellaDati(self):
		self.rettangoli = []
		self.labels = []
		self.linee = []
		self.valoriUsati = []
		
		self.update()

	def popolamentoDati(self, soluzione):
		# Reset dati
		self.cancellaDati()

		# Generazione rettangoli colorati con etichette e valori di riferimento
		for paziente in soluzione.pazienti.values():
			for tipo, start in paziente.esami.items():
				x = start.valore * self.scala + self.offsetx
				y = (2 - paziente.ambulatorio) * self.altezza + self.offsety
				
				# Aggiunta rettangolo
				self.rettangoli.append([QtCore.QRect(QtCore.QPoint(x, y), QtCore.QSize(getattr(self.config, "durata" + str(tipo)) * self.scala, self.altezza)), self.colori[tipo - 1]])
				
				# Aggiunta labels
				if start.valore not in self.valoriUsati:
					self.labels.append([QtCore.QRect(QtCore.QPoint(x - 25, self.compAssey + self.offsetLabely), QtCore.QSize(50,20)), str(start.valore)])
					self.linee.append(QtCore.QLine(QtCore.QPoint(x, self.compAssey), QtCore.QPoint(x, self.compAssey + self.offsetLabely)))
					self.valoriUsati.append(start.valore)
				if start.valore + getattr(self.config, "durata" + str(tipo)) not in self.valoriUsati:
					xFine = (start.valore + getattr(self.config, "durata" + str(tipo))) * self.scala + self.offsetx
					self.labels.append([QtCore.QRect(QtCore.QPoint(xFine - 25, self.compAssey + self.offsetLabely), QtCore.QSize(50,20)), str(start.valore + getattr(self.config, "durata" + str(tipo)))])
					self.linee.append(QtCore.QLine(QtCore.QPoint(xFine, self.compAssey), QtCore.QPoint(xFine, self.compAssey + self.offsetLabely)))
					self.valoriUsati.append(start.valore + getattr(self.config, "durata" + str(tipo)))
				# Label raffigurante id paziente e tipo di job
				self.labels.append([QtCore.QRect(QtCore.QPoint(x, y), QtCore.QSize(getattr(self.config, "durata" + str(tipo)) * self.scala, self.altezza)), "P"+str(paziente.id)+" - E"+str(tipo)])
		
		self.linee.append(QtCore.QLine(QtCore.QPoint(self.offsetx, self.compAssey), QtCore.QPoint(soluzione.makeSpan * self.scala + self.offsetx, self.compAssey)))
		self.linee.append(QtCore.QLine(QtCore.QPoint(self.offsetx, self.compAssey), QtCore.QPoint(self.offsetx, self.offsety)))
		
		# Aggiornamento forzato widget
		self.update()
	
	def resizeEvent(self, e):
		self.setAutoFillBackground(True)
		self.update()
		
	def mouseMoveEvent(self, e):
		self.posFinale = e.x()
		self.update()
	
	def mousePressEvent(self, e):
		self.posIniziale = e.x()
		
	def mouseReleaseEvent(self, e):
		self.offsetWindow = self.offsetWindow + self.posIniziale - self.posFinale
		self.posIniziale = 0
		self.posFinale = 0
	
	def paintEvent(self, e):
		self.setPalette(self.pal)
		painter = QtGui.QPainter(self)
		painter.drawText(QtCore.QRect(QtCore.QPoint(10, 0), QtCore.QSize(150, 20)), QtCore.Qt.AlignLeft, self.nome + " " + self.tipo)

		if self.rettangoli:
			spostat = self.offsetWindow + self.posIniziale - self.posFinale
			if spostat < 0:
				spostat = 0
				self.offsetWindow = 0
				self.posIniziale = self.posFinale
			painter.setWindow(spostat, 0, self.width(), self.height())
			painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
			for elemento in self.rettangoli:
				painter.setBrush(elemento[1])
				painter.drawRect(elemento[0])
			for elemento in self.labels:
				painter.drawText(elemento[0], QtCore.Qt.AlignCenter, elemento[1])
			for linea in self.linee:
				painter.drawLine(linea)

class WidgetIstanza(Widget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		del self.valoriUsati # Eredità inutile

	def inizializzaPar(self, conf, nome):
		self.config = conf
		self.nome = nome
		
		self.scala = 	100 	# Scala dell'intero grafico
		self.altezza = 	30 	# Altezza dei rettangoli
		self.offsetx = 	50 	# Distanza dalla coordinata 0
		self.offsety = 	50 	# Distanza dalla coordinata 0 
		self.offsetLabelx = 10 # Distanza tra asse X e labels
		self.compAssey = self.altezza * 5 + self.offsety # Altezza dell'origine O
		
		# Dimensioni label
		self.labelx = 500
		self.labely = 20

	def cancellaDati(self):
		self.rettangoli = []
		self.labels = []
		self.linee = []
		self.update()

	def popolamentoDati(self, istanza):
		# Reset dei dati
		self.cancellaDati()
	
		# Generazione rettangoli colorati per ogni paziente
		for indicePaziente, paziente in enumerate(istanza):
			for esame in paziente:
				x = indicePaziente * self.scala + self.offsetx
				y = (5 - esame) * self.altezza + self.offsety
				self.rettangoli.append([QtCore.QRect(QtCore.QPoint(x, y), QtCore.QSize(1 * self.scala, self.altezza)), self.colori[esame - 1]])

				# Label
				self.labels.append([QtCore.QRect(QtCore.QPoint(x - self.labelx / 2 + self.scala / 2, self.compAssey + self.offsetLabelx), QtCore.QSize(self.labelx, self.labely)), str(indicePaziente + 1)])

		# Creazione assi cartesiani e labels asse y
		self.linee.append(QtCore.QLine(QtCore.QPoint(self.offsetx, self.compAssey), QtCore.QPoint(len(istanza) * self.scala + self.offsetx, self.compAssey)))
		self.linee.append(QtCore.QLine(QtCore.QPoint(self.offsetx, self.compAssey), QtCore.QPoint(self.offsetx, self.offsety)))
		for tipoEsame in range(1,6):
			y = (5 - tipoEsame) * self.altezza + self.offsety
			self.labels.append([QtCore.QRect(QtCore.QPoint(0 - (self.labelx - 50) / 2, y + ((self.altezza - self.labely) / 2)), QtCore.QSize(self.labelx, self.labely)), "Esame "+str(tipoEsame)])
		# Aggiornamento forzato widget
		self.update()