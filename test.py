import weightedgraph
import random
import queue
model=weightedgraph.Diweightedgraph(20)
for _ in range(30):
    model.addedge(random.uniform(-2.0,2.0),random.randint(0,20),random.randint(0,20))
print(len(model.negtivecycle()))
print(model.bellmanfordSP(5))