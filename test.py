from config import Config
from istanza import Istanza
from euristica import Greedy as g2
from sa import SA as s2
conf = Config()
i = Istanza(conf)
ni = i.nuovaIstanza()
gb = g2(conf)
sol = gb.nuovaGreedy(ni)

print(sol)
#sa2 = s2(conf)
#sol2 = sa2.sa(sol)