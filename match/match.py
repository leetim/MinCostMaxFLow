#!/usr/bin/env python

import machine as m

template = raw_input()
nfa = m.NFA(template)
n = int(raw_input())
for i in range(n):
    s = raw_input()
    print nfa.match(s)
