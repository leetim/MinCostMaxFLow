text, n, *strs = open("input.txt").read().split()
out = open("output.txt", "w")
go_count = 0
div_count = 0
add_list_count = 0

text = "bar"
edges = list()
reference = list()
def sub_str(i, n):
    return text[i:i+n]

def add_vert(ref = None):
    i = len(edges)
    edges.append([None for i in range(26)])
    reference.append(ref)
    return i

def add_edge(v, e):
    c = text[e.k]
    edges[v][ord(c)-ord('a')] = e

def get_edge(v, c):
    return edges[v][ord(c)-ord('a')]

def comp_sub_str(i, j, n):
    if i == j:
        return True
    for k in range(n):
        if text[i+k] != text[j+k]:
            return False
    return True

class Edge:
    def __init__(self, src, to, k, n):
        self.src = src
        self.to = to
        self.k = k
        self.n = n

    def div(self, n):
        global div_count
        div_count += 1
        # ref = go_to(reference[self.src])
        # normalize_ref(self.src)
        ref = reference[self.src]
        ref_v, ref_k, ref_n = ref
        if ref_n == 0:
            ref = go_to((ref_v, self.k, n))
            if ref == None:
                # print(sub_str(self.k, n), (ref_v, k, n))
                print(123)
                1/0

        else:
            ref = go_to((ref_v, ref_k, ref_n+n))
        v = add_vert(ref)
        n_edge = Edge(v, self.to, self.k+n, self.n-n)
        self.to = v
        self.n = n
        add_edge(v, n_edge)
        return v

def go_to(ref):
    v, k, n = ref
    if n == 0:
        return ref
    global go_count
    go_count += 1
    e = get_edge(v, text[k])
    if e == None:
        return None
    if e.n == 1 and e.k == -1:
        return go_to((e.to, k+1, n-1))
    if n >= e.n and text[k] == text[e.k]:#sub_str(k, e.n) == sub_str(e.k, e.n):
        return go_to((e.to, k+e.n, n-e.n))
    if n < e.n and text[k] == text[e.k]:#sub_str(k, n) == sub_str(e.k, n):
        return ref

def check(p, c):
    v, k, n = p
    if n == 0:
        e = get_edge(v, c)
        return e == None
    else:
        e = get_edge(v, text[k])
        if text[e.k] == text[k]:
            return text[e.k+n] != c
    return True

def add_list(root, k):
    global add_list_count
    add_list_count += 1
    add_edge(root, Edge(root, None, k, len(text)))

def normalize_ref(v):
    if reference[v][1] < 0 or reference[v][2] == 0:
        return
    reference[v] = go_to(reference[v])

def in_str(root, s):
    v = root
    while len(s) > 0:
        temp = v
        e = get_edge(v, s[0])
        if e == None:
            return False
        k, n = e.k, e.n
        if n <= len(s) and s[:n] == sub_str(k, n):
            v = e.to
            s = s[n:]
            continue
        if n > len(s) and s == sub_str(k, len(s)):
            return True
        if temp == v:
            return False
    return True

dig = add_vert()
root = add_vert(dig)
reference[dig] = (dig, -1, 0)
reference[root] = (dig, -1, 0)
for i in set(text):
    for k in range(len(text)):
        if text[k] == i:
            add_edge(dig, Edge(dig, root, k, 1))
            break
ep = (root, -1, 0)
for i, c in enumerate(text):
    ap = ep
    while check(ap, c):
        v, k, n = ap
        if n != 0:
            e = get_edge(v, text[k])
            if comp_sub_str(k, e.k, n):#sub_str(e.k, n) == sub_str(k, n):
                v = e.div(n)
        add_list(v, i)
        normalize_ref(v)
        ap = reference[v]
    v, k, n = ap
    if n == 0:
        ep = go_to((v, i, 1))
    else:
        ep = go_to((v, k, n+1))

res = [1 if in_str(root, s) else 0 for s in strs]
for i in res:
    out.write("%d "%i)
out.write("\n")
# print("go_to count: ", go_count)
# print("add_list count: ", add_list_count)
# print("div count: ", div_count)
