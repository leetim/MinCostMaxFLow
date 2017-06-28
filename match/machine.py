from analyse import *

class Edge:
    def __init__(self, src, to, node):
        self.src = src
        self.to = to
        self.node = node

class NFA:
    def __init__(self, template):
        g = GenerTrees("(%s)$"%template)
        node = g.parse_str()
        # node.print_tree()
        self.arr = list()
        self.start = self.add_state()
        self.finish = self.add_state()
        self.add_edge(self.start, self.finish, node)
        e = self.arr[self.start][0]
        e.node.expand(self, e)
        # for L in self.arr:
        #     print [(x.to, x.node) for x in L]

    def add_state(self):
        s = len(self.arr)
        self.arr.append(list())
        return s
    def print_it(self):
        for L in self.arr:
            print [(j.to, j.node) for j in L]
    def add_edge(self, src, to, node):
        self.arr[src].append(Edge(src, to, node))
        return self.arr[src][len(self.arr[src])-1]

    def delta(self, src, sym):
        res = set()
        for e in self.arr[src]:
            if e.node == sym:
                res.add(e.to)
            if e.node == "\0":
                res = res | self.delta(e.to, sym)
        return res

    def match(self, string):
        cur = {self.start}
        can_go = [cur]
        for c in string + "$":
            n_cur = set()
            for s in cur:
                n_cur = n_cur | self.delta(s, c)
            can_go.append(n_cur)
            cur = n_cur
        # print can_go
        return self.finish in cur
