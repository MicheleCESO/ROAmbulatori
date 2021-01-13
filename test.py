from config import Config
from istanza import Istanza
from euristica import Greedy as g1
from sa import SA as s1
from random import seed
from pathRelinking import PathRelinking as PR
seed(1000)
conf = Config()
i = Istanza(conf)
ni = i.nuovaIstanza()

ga = g1(conf)
solg = ga.nuovaGreedy(ni)
solf = ga.nuovaGreedy(ni)
sa1 = s1(conf)
sol1 = sa1.sa(solg)
sol2 = sa1.sa(sol1)

print("\n\n\n\n---- FINITO ----\n")
print(solg.energia,sol1.energia,sol2.energia)
input()
print(len(sol1.pazienti))
path = PR(conf)
m1=sol1.generaMatricePosizione()
m2=sol2.generaMatricePosizione()
diversi=0
for i in range(len(m1)):
	for j in range(len(m1[i])):
		try:
			if m1[i][j] != m2[i][j]:
				diversi+=1
		except IndexError:
				diversi+=1
print("diversi: ",diversi)
ss = path.main(sol1,sol2)#sol1,sol2)
print(ss,"\n\n",ss.energia,"\n",len(ss.pazienti))