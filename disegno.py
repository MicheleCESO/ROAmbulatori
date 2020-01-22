from tkinter import *

def disegna(dati, pi):
	colori = {1:"red",2:"blue",3:"yellow",4:"orange",5:"pink"} # Colori dei diversi jobs

	scala = 30
	offset = 10
	altezza = 50
	i = 0

	# Inizializzazione finestra grafica
	root = Tk()
	root.geometry("1500x220")
	canvas = Canvas(root,width=1500,height=220)
	scrollbar = Scrollbar(root,orient=HORIZONTAL)
	scrollbar.pack(side = BOTTOM,fill = X)
	scrollbar.config(command=canvas.xview)
	canvas.config(xscrollcommand=scrollbar.set)
	canvas.pack()
	
	# Generazione rettangoli colorati con etichette e valori di riferimento
	for idPaziente in dati:
		for chiave, valore in dati[idPaziente].items():
			if chiave != 0:
				x1 = valore[0] * scala + offset
				y1 = (2 - dati[idPaziente][0]) * altezza + offset
				x2 = (valore[0] + pi[chiave]) * scala + offset
				y2 = y1 + altezza
				print(valore[0],pi[chiave],x1,x2,y1,y2)
				canvas.create_rectangle(x1,y1,x2,y2,fill=colori[chiave])
				canvas.create_text((x1+x2)/2,(y1+y2)/2,text=str(chiave)+" P"+str(i))
				canvas.create_line(x2,160,x2,180)
				canvas.create_text(x2,200,text=str(valore[0]+pi[chiave]))
		i += 1
	# Piano cartesiano
	canvas.create_line(10,10,10,160,width=3)
	canvas.create_line(10,160,1500,160,width=3)
	canvas.create_line(10,160,10,180)
	canvas.create_text(10,200,text="0")
	mainloop()