from PyQt5 import QtWidgets, uic, QtGui, QtCore
import pyqtgraph as pg
import sys
from time import sleep
import euristica

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, app, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.app = app
		uic.loadUi("GUI2.ui", self)
		color = self.palette().color(QtGui.QPalette.Window)
		self.graphWidget.setBackground("g")
		self.graphWidget.setLabel('left', "Energia", **{"color":"magenta","font-size":"10pt"})
		self.graphWidget.setLabel('bottom', "Temperatura", **{"color":"magenta","font-size":"10pt"})
		self.graphWidget.showGrid(x=True, y=True)
		self.graphWidget.setXRange(0, 1100, padding=0)
		self.graphWidget.setYRange(0, 60, padding=0)
		self.pen = pg.mkPen(color=(255,0,0), width=1, style=QtCore.Qt.DotLine)
		self.ref = self.graphWidget.plot(pen=self.pen)
		self.start.clicked.connect(lambda: euristica.main(self))
		self.stop.clicked.connect(self.resetGrafico)
		self.x = []
		self.y = []
		self.running = True
		#self.statusbar.showMessage("Ready")
		self.statusBar().addPermanentWidget(self.boxBar)
		self.minimoPazienti.setText("100")
	
	def resetGrafico(self):
		self.ref.clear()
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
			sleep(0.05)
		self.start.setEnabled(True)
	
	def timeStart(self):
		self.timer = QtCore.QTimer()
		self.timer.setInterval(50)
		self.timer.timeout.connect(self.draw)
		self.timer.start()
	
	def draw(self):
		global app
		from random import randint
		self.x.append(100-len(self.x))
		self.y.append(randint(2,50))
		self.ref.setData(self.x,self.y)
		self.temperatura.setNum(100-len(self.x))
		
		#self.widget.update()
		self.app.processEvents()
		#self.graphWidget.plot([1,2,3,4,5,6,7,8,9,10],[30,32,34,32,33,31,29,32,35,45], pen=pen)

	def closeEvent(self, e):
		self.running = False

class Widget(QtGui.QWidget):		
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.aggiorna = False

	def paintEvent(self, e):
		if self.aggiorna:
			painter = QtGui.QPainter(self)
			painter.setPen(QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine))
			#painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
			painter.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.DiagCrossPattern))

			painter.drawRect(100, 0,100,100)
		else:
			painter = QtGui.QPainter(self)
			painter.eraseRect(0,0,1000,1000)

	def passaggioFlag(self, flag):
		print("Flag: ",flag)
		self.aggiorna = flag
		self.update()
		
def main():
	
	app = QtWidgets.QApplication(sys.argv)
	main = MainWindow(app)
	main.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()