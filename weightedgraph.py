import queue
#基于加权边的图算法
class weightededge(object):
    #带权重的无向边
    def __init__(self,weight,u,v):
        self.weight=weight
        self.u=u
        self.v=v
    def either(self):
        return self.v
    def other(self,x):
        if x==self.u:
            return self.v
        elif x== self.v:
            return self.u
        else :
            print("the node isn't existed in the edge")
            return None
    def compareto(self,e):
        return self.weight-e.weight
#基于无向加权边的图算法(最小生成树)
class weightedgraph(object):
    def __init__(self,max):
        self.gra=[]
        for _ in range(max):
            self.gra.append([])

    def addedge(self,weight,u,v):
        a=max(u,v)
        if a>=len(self.gra):
            for _ in range(a-len(self.gra)+1):
                self.gra.append([])
        self.gra[u].append(weightededge(weight,u,v))
        self.gra[v].append(weightededge(weight,u,v))

    def count_edge(self):
        count=0
        for i in range(0,len(self.gra)):
            count+=len(self.gra[i])
        return count/2
#基于Prim算法的最小生成树
    def PrimMST(self):
        weightto=[float('inf')]*len(self.gra)
        pq=queue.PriorityQueue()
        pq.put((0.0,0))
        while not pq.empty():
            (weight,u)=pq.get()
            if not weightto[u]==float('inf'):
                continue
            weightto[u]=weight
            for edge in self.gra[u]:
                pq.put((edge.weight, edge.other(u)))
        return weightto
#加权有向边
class Diweightedge(object):
    def __init__(self,weight,point_from,point_to):
        self.point_from=point_from
        self.point_to=point_to
        self.weight=weight
#加权有向图类，最短路径算法
class Diweightedgraph(object):
    def __init__(self,max):
        self.gra=[]
        for _ in range(max):
            self.gra.append([])
    def addedge(self,weight,p_f,p_t):
        a = max(p_f, p_t)
        if a >= len(self.gra):
            for _ in range(a - len(self.gra) + 1):
                self.gra.append([])
        self.gra[p_f].append(Diweightedge(weight,p_f,p_t))
    #边松弛
    def edgerelax(self,edge):
        u=edge.point_from
        v=edge.point_to
        if self.distance[v]>self.distance[u]+edge.weight:
            self.distance[v]=self.distance[u]+edge.weight
            self.edgeto[v]=u
    #顶点松弛
    def pointrelax(self,v):
        for edge in self.gra[v]:
            u=edge.point_to
            if self.distance[u]<self.distance[v]+edge.weight:
                self.distance[u]=self.distance[v]+edge.weight
                self.edgeto[u]=v
    #检测是否有负权重
    def hasnegweight(self):
        for i in range(len(self.gra)):
            for edge in self.gra[i]:
                if edge.weight<0:
                    return True
        return False
    #检测是否有环
    def hascycle(self):
        self.onstack=[False]*len(self.gra)
        self.mark=[False]*len(self.gra)
        for i in range(len(self.gra)):
            if self.mark[i]==False:
                if self._cyclesearch(i)==True:
                    return True
        return False
    def _cyclesearch(self,v):
        self.onstack[v]=True
        for edge in self.gra[v]:
            w=edge.point_to
            if self.mark[w]==False:
                self.mark[w]=True
                if self._cyclesearch(w)==True:
                    return True
            elif self.onstack[w]==True:
                return True
        self.onstack[v]=False
    #Dijkstra算法，不能处理负权重
    def Dijkstra(self,start):
        assert self.hasnegweight()==False,"Dijkstra algrithm can't process graph with negtive weight"
        distance=[float('inf')]*len(self.gra)
        edgeto=[None]*len(self.gra)
        pq=queue.PriorityQueue()
        distance[start]=0.0
        for i in self.gra[start]:
            pq.put((i.weight,i))
        while not pq.empty():
            (_,edge)=pq.get()
            if distance[edge.point_to]==float('inf'):
                distance[edge.point_to]=distance[edge.point_from]+edge.weight
                edgeto[edge.point_to]=edge.point_from
                for e in self.gra[edge.point_to]:
                    pq.put((e.weight,e))
        return distance,edgeto
    def Topological(self):
        self.stack=[]
        self.mark=[False]*len(self.gra)
        for i in range(len(self.gra)):
            if self.mark[i]==False:
                self._dps_topo(i)
        return self.stack[::-1]
    def _dps_topo(self,v):
        self.mark[v]=True
        for edge in self.gra[v]:
            w=edge.point_to
            if self.mark[w]==False:
                self._dps_topo(w)
        self.stack.append(v)
    #对于无环加权有向图，最高效的算法即为按拓扑排序顺序放松顶点
    def Topo(self,start):
        assert self.hascycle()==False,"Topological algrithm can't process a graph with cycle"
        self.distance=[float('inf')]*len(self.gra)
        self.edgeto=[None]*len(self.gra)
        self.distance[start]=0.0
        order=self.Topological()
        for u in order:
            self.pointrelax(u)
        return self.distance,self.edgeto
    #若图中存在负权重环，则寻找负权重环上的顶点的最短路径没有意义.
    def negtivecycle(self):
        cycles=self.cycle()
        negcycles=[]
        for cycle in cycles:
            weight=0.0
            for edge in cycle:
                weight+=edge.weight
            if weight<0:
                negcycles.append(cycle)
        return negcycles

    def cycle(self):
        self.onstack = [False] * len(self.gra)
        self.cycles = []
        self.path = [None] * len(self.gra)
        for i in range(len(self.gra)):
            if self.path[i] is None:
                self.path[i]=Diweightedge(0.0,i,i)
                self._depthsearch(i)
        return self.cycles

    def _depthsearch(self, v):
        self.onstack[v] = True
        for e in self.gra[v]:
            w=e.point_to
            if self.path[w] is None:
                self.path[w] = e
                self._depthsearch(w)
            elif self.onstack[w] == True:
                cycle = []
                x = e  # 若使用x=path[w]，当w为起始点时会出现BUG
                while not x.point_from == w:
                    cycle.append(x)
                    x = self.path[x.point_from]
                cycle.append(x)
                self.cycles.append(cycle)
        self.onstack[v] = False
    #一般情况下的通用最短路径算法:Bellman-ford
    def bellmanfordSP(self,start):
        q=queue.Queue()
        n=len(self.gra)
        onqueue=[False]*n
        distance=[float('inf')]*n
        edgeto=[None]*n
        q.put(start)
        onqueue[start]=True
        distance[start]=0.0
        count=0#为防止负权重导致无限循环，将relax函数的执行次数上限设为顶点数的平方
        max=n*n
        while not q.empty():
            u=q.get()
            onqueue[u]=False
            for edge in self.gra[u]:
                v=edge.point_to
                if distance[v] > distance[u] + edge.weight:
                    distance[v] = distance[u] + edge.weight
                    edgeto[v] = u
                    if onqueue[v]==False:
                        q.put(v)
                        onqueue[v]=True
            count+=1
            if count>=max:
                print('the relax action has been executed too much')
                break
        return distance,edgeto
