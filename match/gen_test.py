from analyse import letters
from sys import argv
from random import randint, seed
l = list(letters)[10:15]
opers_bin = set("|")
opers_unary = list(set("?*"))
if len(argv) != 5:
    print "Need 4 arguments"
    exit()
n, seek_n, m, seek_m = list(map(int, argv[1:]))

def get_template(n, un = True):
    if n == 0:
        return ""
    if n > 3 and randint(0, 10) < 3:
        return "(%s)" % get_template(n-2)
    if n > 3 and randint(0,10) < 4:
        i = randint(0, len(l)-1)
        return "%s|%s"%(l[i], get_template(n-2))
    if n > 1 and randint(0,10) < 4 and un:
        i = randint(0, len(opers_unary)-1)
        return "%s%s"%(opers_unary[i], get_template(n-1, False))
    i = randint(0, len(l)-1)
    return "%s%s" % (l[i], get_template(n-1))

def get_str(m):
    return "".join([l[randint(0, len(l)-1)] for i in range(m)])

seed(seek_n)
print get_template(n)
seed(seek_m)
print m
for i in range(m):
    print get_str(n)
