from PyQt5 import QtWidgets, uic, QtGui, QtCore
import pyqtgraph as pg
import sys
from time import sleep
from euristica import euri
from SA import saGraph

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, app, conf):
		super(MainWindow, self).__init__()
		self.config = conf # Configurazione
		self.app = app
		uic.loadUi("GUI2.ui", self)

		# Inizializzazione valori dei campi input
		self.configuraInput()
		
		# Passaggio parametri a widget
		self.widget.inizializzaPar(conf, "Soluzione corrente")
		self.widgetSolIniziale.inizializzaPar(conf, "Soluzione iniziale")

		self.graphWidget.setBackground("g")
		self.graphWidget.setLabel('left', "Energia", **{"color":"magenta","font-size":"10pt"})
		self.graphWidget.setLabel('bottom', "Temperatura", **{"color":"magenta","font-size":"10pt"})
		self.graphWidget.showGrid(x=True, y=True)
		self.graphWidget.setXRange(0, conf.iterazioni + (conf.iterazioni / 10), padding=0)
		self.graphWidget.setYRange(0, 150 + 15, padding=0)
		self.pen = pg.mkPen(color=(255,0,0), width=1, style=QtCore.Qt.DotLine)
		self.plotcurve = pg.PlotCurveItem()
		self.graphWidget.addItem(self.plotcurve)
		self.graphWidget.scene().sigMouseMoved.connect(self.posit)
		#self.ref = self.graphWidget.plot(pen=self.pen)
		#self.start.clicked.connect(lambda: inizio(self))
		self.start.clicked.connect(self.inizio)
		#self.start.clicked.connect(self.test)
		self.stop.clicked.connect(self.resetGrafico)
		self.x = []
		self.y = []
		self.running = True
		#self.statusbar.showMessage("Ready")
		self.statusBar().addPermanentWidget(self.boxBar)
		self.inizializzaOpzioni()
		#self.minimoPazienti.setText("100")
	
		# Collegamenti input valori
		self.errori = 0
		self.probNEsami = 100
		self.probEsami = 100
		self.minPazienti.editingFinished.connect(lambda: self.controlloInput("minPazienti", self.minPazienti.text(), False))
		self.maxPazienti.editingFinished.connect(lambda: self.controlloInput("maxPazienti", self.maxPazienti.text(), False))
		
		self.p1Esami.editingFinished.connect(lambda: self.controlloInput("p1Esami", self.p1Esami.text(), False))
		self.p2Esami.editingFinished.connect(lambda: self.controlloInput("p2Esami", self.p2Esami.text(), False))
		self.p3Esami.editingFinished.connect(lambda: self.controlloInput("p3Esami", self.p3Esami.text(), False))
		self.p4Esami.editingFinished.connect(lambda: self.controlloInput("p4Esami", self.p4Esami.text(), False))
		self.p5Esami.editingFinished.connect(lambda: self.controlloInput("p5Esami", self.p5Esami.text(), False))
		
		self.pEsame1.editingFinished.connect(lambda: self.controlloInput("pEsame1", self.pEsame1.text(), False))
		self.pEsame2.editingFinished.connect(lambda: self.controlloInput("pEsame2", self.pEsame2.text(), False))
		self.pEsame3.editingFinished.connect(lambda: self.controlloInput("pEsame3", self.pEsame3.text(), False))
		self.pEsame4.editingFinished.connect(lambda: self.controlloInput("pEsame4", self.pEsame4.text(), False))
		self.pEsame5.editingFinished.connect(lambda: self.controlloInput("pEsame5", self.pEsame5.text(), False))
		
		self.temperatura.editingFinished.connect(lambda: self.controlloInput("temperatura", self.temperatura.text(), False))
		self.tassoRaffreddamento.editingFinished.connect(lambda: self.controlloInput("tassoRaffreddamento", self.tassoRaffreddamento.text(), False))
		self.iterazioni.editingFinished.connect(lambda: self.controlloInput("iterazioni", self.iterazioni.text(), False))
	
	def inizio(self):
		ist = [[5], [5], [2, 4, 5, 1], [3], [5, 2], [4], [5, 2], [2, 3, 1, 5], [2], [1], [5, 3, 1], [5], [1, 4], [4], [1, 2, 3]]
		durata = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
		pazienti, jobs, ambulatori = euri(ist, durata)
		res = saGraph(pazienti, jobs, ambulatori, self.config, self)
		print(res)
	
	# Funzione che attribuisce il valore iniziale corretto a tutti i campi input del pannello di configurazione
	def configuraInput(self):
		self.minPazienti.setText(str(self.config.minPazienti))
		self.maxPazienti.setText(str(self.config.maxPazienti))
		self.p1Esami.setText(str(self.config.p1Esami))
		self.p2Esami.setText(str(self.config.p2Esami))
		self.p3Esami.setText(str(self.config.p3Esami))
		self.p4Esami.setText(str(self.config.p4Esami))
		self.p5Esami.setText(str(self.config.p5Esami))
		self.pEsame1.setText(str(self.config.pEsame1))
		self.pEsame2.setText(str(self.config.pEsame2))
		self.pEsame3.setText(str(self.config.pEsame3))
		self.pEsame4.setText(str(self.config.pEsame4))
		self.pEsame5.setText(str(self.config.pEsame5))
		self.temperatura.setText(str(self.config.temperatura))
		self.tassoRaffreddamento.setText(str(self.config.tassoRaffreddamento))
		self.iterazioni.setText(str(self.config.iterazioni))
	
	# Funzione per controllare i valori di input delle impostazioni
	def controlloInput(self, idBottone, valore, ricorsione):
		# Minimi pazienti
		if idBottone == "minPazienti":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto > self.config.maxPazienti or valoreCorretto < 1: # Valore sbagliato
				self.minPazienti.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | 1
			else:
				self.minPazienti.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1)
				self.config.minPazienti = valoreCorretto
				if not ricorsione:
					self.controlloInput("maxPazienti", self.maxPazienti.text(), True)
		# Massimo pazienti
		elif idBottone == "maxPazienti":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < self.config.minPazienti: # Valore sbagliato
				self.maxPazienti.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 1)
			else:
				self.maxPazienti.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 1)
				self.config.maxPazienti = valoreCorretto
				if not ricorsione:
					self.controlloInput("minPazienti", self.minPazienti.text(), True)
		# Probabilità di avere un esame
		elif idBottone == "p1Esami":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.p1Esami.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 2)
			else:
				self.p1Esami.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 2)
				self.config.p1Esami = valoreCorretto
		# Probabilità di avere due esami
		elif idBottone == "p2Esami":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.p2Esami.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 3)
			else:
				self.p2Esami.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 3)
				self.config.p2Esami = valoreCorretto
		# Probabilità di avere tre esami
		elif idBottone == "p3Esami":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.p3Esami.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 4)
			else:
				self.p3Esami.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 4)
				self.config.p3Esami = valoreCorretto
		# Probabilità di avere quattro esami
		elif idBottone == "p4Esami":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.p4Esami.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 5)
			else:
				self.p4Esami.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 5)
				self.config.p4Esami = valoreCorretto
		# Probabilità di avere cinque esami
		elif idBottone == "p5Esami":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.p5Esami.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 6)
			else:
				self.p5Esami.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 6)
				self.config.p5Esami = valoreCorretto
		####################
		# Probabilità di eseguire l'esame uno
		elif idBottone == "pEsame1":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.pEsame1.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 7)
			else:
				self.pEsame1.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 7)
				self.config.pEsame1 = valoreCorretto
		# Probabilità di eseguire l'esame due
		elif idBottone == "pEsame2":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.pEsame2.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 8)
			else:
				self.pEsame2.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 8)
				self.config.pEsame2 = valoreCorretto
		# Probabilità di eseguire l'esame tre
		elif idBottone == "pEsame3":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.pEsame3.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 9)
			else:
				self.pEsame3.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 9)
				self.config.pEsame3 = valoreCorretto
		# Probabilità di eseguire l'esame quattro
		elif idBottone == "pEsame4":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.pEsame4.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 10)
			else:
				self.pEsame4.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 10)
				self.config.pEsame4 = valoreCorretto
		# Probabilità di eseguire l'esame cinque
		elif idBottone == "pEsame5":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Istanze"][idBottone])
			if tipoSbagliato or valoreCorretto < 0 or valoreCorretto > 100:
				self.pEsame5.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 11)
			else:
				self.pEsame5.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 11)
				self.config.pEsame5 = valoreCorretto
		####################
		# Temperatura
		elif idBottone == "temperatura":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Parametri"][idBottone])
			if tipoSbagliato or valoreCorretto < 0:
				self.temperatura.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 14)
			else:
				self.temperatura.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 14)
				self.config.temperatura = valoreCorretto
		# Tasso di raffreddamento
		elif idBottone == "tassoRaffreddamento":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Parametri"][idBottone])
			if tipoSbagliato or valoreCorretto <= 0 or valoreCorretto >= 1:
				self.tassoRaffreddamento.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 15)
			else:
				self.tassoRaffreddamento.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 15)
				self.config.tassoRaffreddamento = valoreCorretto
		# Iterazioni
		elif idBottone == "iterazioni":
			valoreCorretto, tipoSbagliato = self.controlloTipo(valore, self.config.schema["Parametri"][idBottone])
			if tipoSbagliato or valoreCorretto <= 0:
				self.iterazioni.setStyleSheet("color: red; background-color: black;")
				self.errori = self.errori | (1 << 16)
			else:
				self.iterazioni.setStyleSheet("color: black;")
				self.errori = self.errori & ~(1 << 16)
				self.config.iterazioni = valoreCorretto
		####################
		# Controllo sommatorie
		sommaNumeroEsami = self.config.p1Esami + self.config.p2Esami +self.config.p3Esami +self.config.p4Esami +self.config.p5Esami
		if sommaNumeroEsami != 100: # Il totale deve essere 100%
			self.totaleProbNumEsami.setStyleSheet("color: red; background-color: black;")
			self.errori = self.errori | (1 << 12)
		else:
			self.totaleProbNumEsami.setStyleSheet("color: black;")
			self.errori = self.errori & ~(1 << 12)
		self.totaleProbNumEsami.setNum(sommaNumeroEsami)
		sommaTipoEsami = self.config.pEsame1 + self.config.pEsame2 +self.config.pEsame3 +self.config.pEsame4 +self.config.pEsame5
		if sommaTipoEsami != 100: # Il totale deve essere 100%
			self.totaleProbEsami.setStyleSheet("color: red; background-color: black;")
			self.errori = self.errori | (1 << 13)
		else:
			self.totaleProbEsami.setStyleSheet("color: black;")
			self.errori = self.errori & ~(1 << 13)
		self.totaleProbEsami.setNum(sommaTipoEsami)
		if self.errori == 0:
			self.start.setEnabled(True)
			self.config.salva()
		else:
			self.start.setEnabled(False)
	
	# Funzione per verificare se il parametro è un determinato tipo di dato, appartenente alla lista data in input contenente i tipi di dato accettabili
	def controlloTipo(self, par, tipiDato):
		try:
			if type(eval(par)) in tipiDato:
				return eval(par), False
			else:
				return None, True
		except (NameError, SyntaxError):
			print("c")
			return None, True
	
	def posit(self, pos):
		act_pos = self.plotcurve.mapFromScene(pos)
		if self.plotcurve.mouseShape().contains(act_pos):
			print(act_pos)

	def inizializzaOpzioni(self):
		for sezione, parametri in self.config.schema.items():
			for parametro in parametri:
				getattr(self, parametro).setText(str(getattr(self.config, parametro)))

	def resetGrafico(self):
		self.plotcurve.clear()
		self.x = []
		self.y = []

	def pissi(self):
		print("Test")
		self.widget.passaggioFlag(True)
		self.ref.clear()
		self.x = []
		self.y = []
		#self.ref = self.graphWidget.plot(pen=self.pen)
	
	def inverti(self):
		print("Test")
		self.widget.passaggioFlag(False)
	
	def test(self):
		self.resetGrafico()
		self.start.setEnabled(False)
		self.widget.passaggioFlag(True)
		i = 0
		while self.running and i < 100:
			self.draw()
			i += 1
			#sleep(0.05)
		self.start.setEnabled(True)
	
	def draw(self, x, y):
		self.x.append(x)
		self.y.append(y)
		self.plotcurve.setData(self.x, self.y, pen=self.pen)
		
		#self.app.processEvents()
		
	def closeEvent(self, e):
		self.running = False

class Widget(QtGui.QWidget):		
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rettangoli = []
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
		#self.creaOggetti()
		
		
	def inizializzaPar(self, conf, nome):
		self.config = conf
		self.nome = nome
		
		self.scala = 50	# Scala dell'intero grafico
		self.altezza = 30 # Altezza dei rettangoli
		self.offsetx = 50 # Distanza dalla coordinata 0
		self.offsety = 20 # Distanza dalla coordinata 0 
		self.offsetLabely = 10 # Distanza tra asse X e labels
		self.compAssey = self.altezza * 3 + self.offsety # Altezza dell'origine O
		self.durata = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
	
	def creaOggetti(self, dati, soglia):
		self.rettangoli = []
		self.labels = []
		self.linee = []
		self.valoriUsati = []
		# Generazione rettangoli colorati con etichette e valori di riferimento
		for paziente in dati.values():
			for tipo, start in paziente["jobs"].items():
				x = start[0] * self.scala + self.offsetx
				y = (2 - paziente["ambulatorio"]) * self.altezza + self.offsety
				self.rettangoli.append([QtCore.QRect(QtCore.QPoint(x, y), QtCore.QSize(self.durata[tipo] * self.scala, self.altezza)), self.colori[tipo - 1]])
				if start[0] not in self.valoriUsati:
					self.labels.append([QtCore.QRect(QtCore.QPoint(x - 25, self.compAssey + self.offsetLabely), QtCore.QSize(50,20)), str(start[0])])
					self.linee.append(QtCore.QLine(QtCore.QPoint(x, self.compAssey), QtCore.QPoint(x, self.compAssey + self.offsetLabely)))
					self.valoriUsati.append(start[0])
				if start[0] + self.durata[tipo] not in self.valoriUsati:
					xFine = (start[0] + self.durata[tipo]) * self.scala + self.offsetx
					self.labels.append([QtCore.QRect(QtCore.QPoint(xFine - 25, self.compAssey + self.offsetLabely), QtCore.QSize(50,20)), str(start[0] + self.durata[tipo])])
					self.linee.append(QtCore.QLine(QtCore.QPoint(xFine, self.compAssey), QtCore.QPoint(xFine, self.compAssey + self.offsetLabely)))
					self.valoriUsati.append(start[0] + self.durata[tipo])
				# Label raffigurante id paziente e tipo di job
				self.labels.append([QtCore.QRect(QtCore.QPoint(x, y), QtCore.QSize(self.durata[tipo] * self.scala, self.altezza)), "P"+str(paziente["id"])+" - J"+str(tipo)])
		#self.rettangoli.append([QtCore.QRect(QtCore.QPoint(50, 0), QtCore.QSize(100, 30)), self.cyan])
		#self.rettangoli.append([QtCore.QRect(QtCore.QPoint(50, 30), QtCore.QSize(100, 30)), self.magenta])
		#self.rettangoli.append([QtCore.QRect(QtCore.QPoint(50, 60), QtCore.QSize(100, 30)), self.green])
		
		self.asseX = QtCore.QLine(QtCore.QPoint(self.offsetx, self.compAssey), QtCore.QPoint(soglia * self.scala + self.offsetx, self.compAssey))
		self.asseY = QtCore.QLine(QtCore.QPoint(self.offsetx, self.compAssey), QtCore.QPoint(self.offsetx, self.offsety))
		self.label = [QtCore.QPoint(self.offsetx, self.offsety), "25"]
		self.update()
	
	def resizeEvent(self, e):
		print("resize1")
		self.setAutoFillBackground(True)
		self.update()
		print("resize2")
		
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
		painter.drawText(QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QSize(100,20)), QtCore.Qt.AlignCenter, self.nome)
		
		if self.rettangoli:
			spostat = self.offsetWindow + self.posIniziale - self.posFinale
			if spostat < 0:
				print(spostat,self.offsetWindow, self.posIniziale, self.posFinale)
				spostat = 0
				self.offsetWindow = 0
				self.posIniziale = self.posFinale
			painter.setWindow(spostat, 0, self.width(), self.height())
			print(self.width(),self.height(),painter.window(),"---",self.offsetWindow + self.posIniziale - self.posFinale, self.offsetWindow, self.posIniziale, self.posFinale)
			painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
			for elemento in self.rettangoli:
				painter.setBrush(elemento[1])
				painter.drawRect(elemento[0])
			painter.drawLine(self.asseX)
			painter.drawLine(self.asseY)
			for elemento in self.labels:
				painter.drawText(elemento[0], QtCore.Qt.AlignCenter, elemento[1])
			for linea in self.linee:
				painter.drawLine(linea)

	def creaElementiGrafici(self, dati):
		for idPaziente, paziente in dati.items():
			self.rettangoli[idPaziente] = {}
			for tipo, start in paziente["jobs"].items():
				origine = QtCore.QPoint(start[0] * self.lunghezza + self.offset, ) # Coordinate alto - sinistra del job
				dimensioni = QtCore.QSize(self.lunghezza  * self.durata[tipo], self.altezza)
				self.rettangoli[idPaziente][tipo] = QtCore.QRect(origine, dimensioni)
		
		self.update()
		
	def modificaElementiGrafici(self, dati):
		pass