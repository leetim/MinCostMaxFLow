from queue import *
import sys

in_data = list(map(int, sys.stdin.read().split()))
n, e = in_data[0], in_data[1:]
e = [(e[i], e[i+1]) for i in range(0, len(e), 2)]

pair = {i+1:-1 for i in range(n)}
E = {i:list() for i in pair}
for src, to in e:
    E[src].append(to)
    E[to].append(src)

################################################################################
def get_base(way, bases, root, u, v):
    visited = set()
    cur = u
    while True:
        cur = bases[cur]
        visited.add(cur)
        if cur == root:
            break
        cur = way[pair[cur]]
    cur = v
    while True:
        cur = bases[cur]
        if cur in visited:
            break
        cur = way[pair[cur]]
    return cur

def get_cycle_verts(way, bases, curbase, u, v):
    cycle = {u, v}
    while bases[u] != curbase:
        cycle.add(bases[pair[u]])
        u = way[pair[u]]
        cycle.add(bases[u])
    while bases[v] != curbase:
        cycle.add(bases[pair[v]])
        v = way[pair[v]]
        cycle.add(bases[v])
    return cycle

def make_new_ways(way, bases, curbase, u, child):
    while bases[u] != curbase:
        way[u] = child
        child = pair[u]
        u = way[pair[u]]

def mark_cycle(way, bases, root, u, v):
    cycle = set()
    curbase = get_base(way, bases, root, u, v)
    cycle = get_cycle_verts(way, bases, curbase, u, v)
    make_new_ways(way, bases, curbase, u, v)
    make_new_ways(way, bases, curbase, v, u)
    return (curbase, cycle)

def repaired_way(way, root, v):
    while True:
        temp_v = way[v]
        next_v = pair[temp_v]
        pair[v] = temp_v
        pair[temp_v] = v
        v = next_v
        if temp_v == root:
            return
################################################################################

def bfs(root):
    q = Queue()
    visited = {root}
    q.put(root)
    bases = {i:i for i in pair}
    way = {i:-1 for i in pair}
    while not q.empty():
        cur = q.get()
        for v in E[cur]:
            next_v = pair[v]
            if bases[v] == bases[cur] or pair[cur] == v:
                continue
            if root == v or (next_v != -1 and way[next_v] != -1):
                curbase, cycle = mark_cycle(way, bases, root, cur, v)
                for i in pair:
                    if bases[i] in cycle:
                        if not i in visited:
                            q.put(i)
                            visited.add(i)
                        bases[i] = curbase
            else:
                if way[v] == -1:
                    way[v] = cur
                    if next_v == -1 and v != root:
                        repaired_way(way, root, v)
                        return v
                    visited.add(next_v)
                    q.put(next_v)
    return -1
################################################################################

change_flag = True
while change_flag:
    change_flag = False
    for i in pair:
        if pair[i] == -1:
            temp = bfs(i)
            change_flag = change_flag or temp != -1

paired = set()
p = list()
for i in pair:
    if not i in paired and pair[i] != -1:
        p.append((i, pair[i]))
        paired.add(i)
        paired.add(pair[i])
print(len(p)*2)
for i, j in p:
    print(i, j)
