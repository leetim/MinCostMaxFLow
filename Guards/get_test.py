
from sys import argv
import random as r
if len(argv) != 4:
    exit()
n, m, s = map(int, argv[1:])
print(n)
paired = set()
count = 0
r.seed(s)
edges = list()
while count < m:
    src = r.randint(1, n)
    to = r.randint(1, n)
    if not ((src, to) in paired or (to, src) in paired or src == to):
        if src > to:
            temp1 = src
            src = to
            to = temp1
        edges.append((src, to))
        paired.add((src, to))
        count += 1
for i in sorted(edges):
    print("%d %d"%i)
