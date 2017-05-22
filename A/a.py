import queue as Q
other = list(map(int, open("input.txt").read().split()))
big_flow = 10**10
n = other[0]
V = other[1:n+1]

E = [other[1+(i+1)*n:1+(i+2)*n] for i in range(n)]
for i in range(n):
    E[i].append(0)
    E[i].append(0)
E.append([0]*(n+2))
E.append([0]*(n+2))
start = n
finish = n+1

for i in filter(lambda x: V[x]==1, [i for i in range(n)]):
    E[start][i] = big_flow

for i in filter(lambda x: V[x]==2, [i for i in range(n)]):
    E[i][finish] = big_flow

n+=2
F = [[0 for j in range(n)] for i in range(n)]
C = lambda v1, v2: E[v1][v2]-F[v1][v2]

def bfs(v):
    q = Q.Queue(100)
    visited = set()
    stack = list()
    q.put((v, -1))
    while not q.empty():
        t = q.get()
        stack.append(t)
        if t[0] == finish:
            break
        for i in range(n):
            if i in visited:
                continue
            if C(t[0], i) > 0:
                visited.add(i)
                q.put((i, t[0]))
    way=list()
    cur = finish
    for i in stack[::-1]:
        if i[0] == cur:
            cur = i[1]
            way.append(i[0])
    if len(way)==0:
        return -1
    way = way[::-1]
    flow = min(C(way[i], way[i+1]) for i in range(len(way)-1))
    for i in range(len(way)-1):
        F[way[i]][way[i+1]] += flow
        F[way[i+1]][way[i]] -= flow
    return flow

while True:
    # visited = [0]*n
    k = bfs(start)
    if k < 0:
        break

res = sum(F[j][finish] for j in range(n))
out = open("output.txt", "w")
out.write(str(res) + "\n")
