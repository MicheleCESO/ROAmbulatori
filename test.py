from config import Config
from istanza import Istanza
from euristica import Greedy as g1
from sa import SA as s1
from random import seed
from pathRelinking import PathRelinking as PR

conf = Config()
i = Istanza(conf)
ni = i.nuovaIstanza()

ga = g1(conf)
solg = ga.nuovaGreedy(ni)
sa1 = s1(conf)
sol1 = sa1.sa(solg)
sol2 = sa1.sa(sol1)

print("\n\n\n\n---- FINITO ----\n")
print(sol1.energia,sol2.energia)
path = PR(conf)
ss = path.main(sol1,sol2)
print(ss,"\n\n",ss.energia,"\n",len(ss.pazienti))