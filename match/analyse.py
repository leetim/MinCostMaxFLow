
letters = set("$ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
class Node:
    def __init__(self, c, ch = None):
        self.__c = c
        if ch == None:
            self.__ch = list()
        else:
            self.__ch = ch
    def print_tree(self, lvl = 0):
        print( "    "*max(lvl-1, 0) + "|---"*min(lvl, 1) + self.__c)
        for i in self.__ch:
            i.print_tree(lvl + 1)
            # if i != None:
    def get_char(self):
        return self.__c
    def add_symb(self, c):
        self.__ch.append(c)
    def get_symbs(self):
        return self.__ch
    def expand(self, nfa, edge):
        return

class NodeSymb(Node):
    def __init__(self, c):
        Node.__init__(self, c, [])
    def expand(self, nfa, edge):
        edge.node = self.get_char()

class NodeConcat(Node):
    def __init__(self, ch = None):
        Node.__init__(self, "concat", ch)
    def expand(self, nfa, edge):
        start = edge.src
        finish = edge.to
        symbs = self.get_symbs()
        # print list(reversed(symbs))[:len(symbs)-1]
        for i in list(reversed(symbs))[:len(symbs)-1]:
            s = nfa.add_state()
            ne = nfa.add_edge(s, edge.to, i)
            i.expand(nfa, ne)
            edge.to = s
        edge.node = symbs[0]
        symbs[0].expand(nfa, edge)


class NodeOr(Node):
    def __init__(self, ch1 = None, ch2 = None):
        Node.__init__(self, "or", [ch1, ch2])

    def expand(self, nfa, edge):
        start = edge.src
        finish = edge.to
        ch1, ch2 = self.get_symbs()
        ne = nfa.add_edge(start, finish, ch1)
        edge.node = ch2
        ch1.expand(nfa, ne)
        ch2.expand(nfa, edge)

class NodeRep1(Node):
    def __init__(self, ch):
        Node.__init__(self, "?", [ch])

    def expand(self, nfa, edge):
        start = edge.src
        finish = edge.to
        s = nfa.add_state()
        ch = self.get_symbs()[0]
        ne1 = nfa.add_edge(s, finish, ch)
        ne2 = nfa.add_edge(s, s, ch)
        edge.node = "\0"
        edge.to = s
        ch.expand(nfa, ne1)
        ch.expand(nfa, ne2)

class NodeRep0(Node):
    def __init__(self, ch):
        Node.__init__(self, "*", [ch])

    def expand(self, nfa, edge):
        start = edge.src
        finish = edge.to
        s = nfa.add_state()
        ch = self.get_symbs()[0]
        ne1 = nfa.add_edge(s, finish, ch)
        ne2 = nfa.add_edge(s, s, ch)
        edge.node = "\0"
        edge.to = s
        ch.expand(nfa, ne1)
        ch.expand(nfa, ne2)
        nfa.add_edge(start, finish, "\0")

class GenerTrees:
    def __init__(self, string):
        self.set_str(string)

    def set_str(self, string):
        self.string = string
        self.pos = 0

    def next(self):
        self.pos += 1

    def check_symb(self, symb):
        if self.cur() == symb:
            return True
        raise ValueError, "Need %s in str"%symb

    def cur(self):
        if self.check_end_of_str():
            return self.string[self.pos]
        return "\0"

    def check_end_of_str(self):
        return self.pos < len(self.string)

    def parse_symb(self):
        if self.cur() == "(":
            self.next()
            return self.parse_str(")")
        temp = NodeSymb(self.cur())
        self.next()
        return temp

    def parse_escape(self):
        self.next()
        temp = NodeSymb(self.cur())
        self.next()
        return temp

    def parse_rep0(self, end_symb):
        self.next()
        ch = self.parse_symb()
        return NodeRep0(ch)

    def parse_rep1(self, end_symb):
        self.next()
        ch = self.parse_symb()
        # ch = self.parse_str(end_symb)
        return NodeRep1(ch)

    def parse_str(self, end_symb = "\0"):
        concat = list()
        while self.cur() != end_symb:
            # print self.cur()
            cur = self.cur()
            if cur == "\\":
                concat.append(self.parse_escape())
                continue
            if cur == "*":
                concat.append(self.parse_rep0(end_symb))
                continue
            if cur == "?":
                concat.append(self.parse_rep1(end_symb))
                continue
            if cur == "|":
                self.next()
                left = None
                if len(concat) > 1:
                    left = NodeConcat(concat)
                else:
                    left = concat[0]
                right = self.parse_str(end_symb)
                return NodeOr(left, right)
            concat.append(self.parse_symb())
        self.next()
        if len(concat) > 1:
            return NodeConcat(concat)
        else:
            return concat[0]
