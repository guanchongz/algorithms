from collections import deque
#基础图算法类
class graph(object):
    def __init__(self,max):
        self.gra=[]
        for _ in range(max+1):
            self.gra.append([])
    def addedge(self,v,w):
        assert max(v,w)<len(self.gra),'add edge:point out of range'
        if w not in self.gra[v] :
            self.gra[v].append(w)
        if v not in self.gra[w] :
            self.gra[w].append(v)
    def addnode(self,v):
        for i in range(len(self.gra),v+1):
            self.gra.append([])
    def node_max(self):
        return len(self.gra)-1
    def count_edge(self):
        count=0
        for i in range(0,len(self.gra)):
            count+=len(self.gra[i])
        return count/2
    def neighbor(self,v):
        if v>=len(self.gra):
            return
        return self.gra[v]
    #深度优先搜索，path实现了路径记录和到达标记两种功能，节省了时间和空间
    def depthsearch(self,start):
        assert start<len(self.gra),'search:point out of range'
        self.path=[None]*len(self.gra)
        self.path[start]=-1
        self._depthsearch(start)
        return self.path
    def _depthsearch(self,v):
        for i in self.gra[v] :
            if self.path[i] is None:
                self.path[i]=v
                self._depthsearch(i)
    def linked(self,v,w):
        if w>=len(self.gra) or v>=len(self.gra) :
            return None
        p=self.breadthsearch(v)
        if p[w] :
            self.stack=[w]
            while not p[w]=='s':
                w=p[w]
                self.stack.append(w)
            return self.stack
        else :
            return False
    def show(self):
        for i in range(0,len(self.gra)):
            print(self.gra[i])
    #广度优先搜索
    def breadthsearch(self,start):
        assert start < len(self.gra), 'search:point out of range'
        self.path=[None]*len(self.gra)
        self.path[start]=-1
        self.queue = deque([start])
        self._breadthsearch(start)
        return self.path
    def _breadthsearch(self,v):
        while v>=0 :
            for i in self.gra[v]:
                if not self.path[i]:
                    self.queue.append(i)
                    self.path[i]=v
            try:
                v=self.queue.popleft()
            except:
                v=-1
#符号图
class symbolgraph(graph):
    def __init__(self,max):
        self.dict={}
        self.key=[]
        super().__init__(max)
    def addedge(self,v,w):
        if v not in self.key:
            self.key.append(v)
            self.dict.update({v:(len(self.key)-1)})
        if w not in self.key:
            self.key.append(w)
            self.dict.update({w:(len(self.key)-1)})
        if len(self.gra)<=len(self.key):
            for i in range(10):
                self.gra.append([])
        if self.dict[w] not in self.gra[self.dict[v]]:
            self.gra[self.dict[v]].append(self.dict[w])
        if self.dict[v] not in self.gra[self.dict[w]]:
            self.gra[self.dict[w]].append(self.dict[v])
    def linked(self,p,q):
        if (p not in self.key) or( q not in self.key):
            return False
        self.l=self.breadthsearch(self.dict[p])
        if self.l[self.dict[q]]:
            return True
        else :
            return False
    def neighbor(self,p):
        if p not in self.key:
            return None
        self.l=self.breadthsearch(self.dict[p])
        return [self.key[i] for i in range(len(self.gra)) if self.l[i] and self.l[i]>=0 ]
#有向图
class Digraph(graph):
    def __init__(self,max):
        super().__init__(max)
    def addedge(self,u,v):
        a=max(u,v)
        if a>=len(self.gra):
            for i in range(a-len(self.gra)):
                self.gra.append([])
        if v not in self.gra[u]:
            self.gra[u].append(v)
    #返回有向图中所有的环
    def cycle(self):
        self.onstack=[False]*len(self.gra)
        self.cycles=[]
        self.path = [None] * len(self.gra)
        for i in range(len(self.gra)):
            if self.path[i] is None:
                self.path[i]=i
                self._depthsearch(i)
        return self.cycles
    def _depthsearch(self,v):
        self.onstack[v]=True
        for w in self.gra[v]:
            if self.path[w] is None:
                self.path[w]=v
                self._depthsearch(w)
            elif self.onstack[w]==True:
                cycle=[w]
                x=v#若使用x=path[w]，当w为起始点时会出现BUG
                while not x==w :
                    cycle.append(x)
                    x=self.path[x]
 #                   print('cycle:',x)
                cycle.append(x)
                self.cycles.append(cycle)
        self.onstack[v]=False
    #检查有向图中是否有环（此函数效率要比cycle高）
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
        for w in self.gra[v]:
            if self.mark[w]==False:
                self.mark[w]=True
                if self._cyclesearch(w)==True:
                    return True
            elif self.onstack[w]==True:
                return True
        self.onstack[v]=False
    #基于深度优先搜索的拓扑排序，其中使用栈实现逆后序排序
    def Topological(self):
        assert self.hascycle()==False,'there is one cycle in the graph at least'
        self.stack=[]
        self.mark=[False]*len(self.gra)
        for i in range(len(self.gra)):
            if self.mark[i]==False:
                self._dps_topo(i)
        return self.stack[::-1]
    def _dps_topo(self,v):
        self.mark[v]=True
        for w in self.gra[v]:
            if self.mark[w]==False:
                self._dps_topo(w)
        self.stack.append(v)
