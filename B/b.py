from queue import *
inf = 10**13
in_data = list(map(int, open("brides.in").read().split()))
n, m, k = in_data[:3]
A = ([in_data[i*3:(i+1)*3] + [i] for i in range(1, m+1)])
################################################################################
n+=1
start = 0
finish = n-1
phi = [0 for i in range(n)]
phi[finish] = 0
################################################################################
class Edge:
    def __init__(self, src, to, cost, flow, max_capacity, ind):
        self.src = src
        self.to = to
        self.cost = cost
        self.new_cost = cost
        self.flow = flow
        self.ind = ind
        self.max_capacity = max_capacity
    def get_cap(self):
        return self.max_capacity - self.flow
    def get_cost(self):
        return self.cost + phi[self.to] - phi[self.src]
    def print_edge(self):
        return ("(%d, %d, %d, %d)"%(self.src, self.to, self.ind, self.flow))
    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

################################################################################
E = [list() for i in range(n)]
E_back = [list() for i in range(n)]
E[0].append(Edge(0, 1, 0, 0, k, 0))
E[1].append(Edge(1, 0, 0, 0, 0, 0))
E_back[0].append(Edge(0, 1, 0, 0, 0, 0))
E_back[1].append(Edge(1, 0, 0, 0, k, 0))
for t in A:
    E[t[0]].append(Edge(t[0], t[1], t[2], 0, 1, t[3]))
    E[t[1]].append(Edge(t[1], t[0], t[2], 0, 1, t[3]))
    E[t[0]].append(Edge(t[0], t[1], -t[2], 0, 0, -t[3]))
    E[t[1]].append(Edge(t[1], t[0], -t[2], 0, 0, -t[3]))
for i in E:
    for j in i:
        E_back[j.to].append(j)
def get_back(e):
    for eb in E[e.to]:
        if eb.ind == -e.ind and eb.src == e.to:
            return eb
    return None

################################################################################
def dijkstr():
    visited = set()
    verts = [[inf, i, None] for i in range(n)]
    verts[finish][0] = 0
    q = PriorityQueue()
    q.put(verts[finish].copy())
    while not q.empty():
        val, t, e = q.get()
        if t in visited:
            continue
        visited.add(t)
        for eb in E_back[t]:
            if eb.get_cap() > 0:
                if verts[eb.src][0] > verts[eb.to][0] + eb.get_cost():
                    verts[eb.src] = [verts[eb.to][0] + eb.get_cost(), eb.src, eb]
                    q.put(verts[eb.src].copy())
    if verts[start][0] == inf:
        return 0
    for i in range(n):
        phi[i] += verts[i][0]
    cur = start
    way = list()
    while cur != finish:
        val, t, e = verts[cur]
        e.flow += 1
        be = get_back(e)
        be.flow -= 1
        cur = e.to
    return 1

################################################################################
temp = 1
while temp > 0:
    temp = dijkstr()
flow_val = sum([j.flow for j in filter(lambda x: x.flow > 0, E[start])])

################################################################################
way = list()
visited = set()
def get_way(v = start):
    if v == start:
        way.clear()
        visited.clear()
    if v == finish:
        return True
    if v in visited:
        return False
    visited.add(v)
    for e in E[v]:
        if e.flow > 0:
            if get_way(e.to):
                way.append(e)
                return True

################################################################################
out = open("brides.out", "w")
if flow_val < k:
    out.write("-1\r\n")
    exit()
res = float(sum(sum(e.cost for e in filter(lambda x: x.flow > 0, L)) for L in E))/k
ways = list()
for i in range(k):
    get_way()
    ways.append(way[::-1])
    for i in way:
        i.flow -= 1
out.write("%0.5f\r\n"%res)
for i in ways:
    out.write("%d"%len(i[1:]))
    for j in i[1:]:
        out.write(" %d"%j.ind)
    out.write("\r\n")
