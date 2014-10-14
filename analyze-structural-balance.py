# -*- coding: utf-8 -*-
import pickle
import networkx as nx
import sys
import re

G = nx.DiGraph()

p = re.compile("([0-9]+)[ \t]+([0-9]+)[ \t]+([-+0-9]+).*")
with open(sys.argv[1]) as f:
    for line in f:
        if line[0] == "#":
            continue
        
        m = p.match(line)
        G.add_edge(int(m.group(1)), int(m.group(2)), weight=int(m.group(3)))

def check_for_self_loops(triangle):
    return len(set(reduce(lambda acc, x: acc + x, triangle))) is not 3
def get_unique(triangle):
    return tuple(sorted(set(reduce(lambda acc, x: acc + x, triangle))))
def get_sign(G, triangle):
    return tuple(map(lambda e: int(G[e[0]][e[1]]['weight']), triangle))
def check_for_structural_balance(signed_triangle):
    sum_t = sum(signed_triangle)
    return sum_t is 3 or sum_t is 1



triangles = {}
for fn in range(len(sys.argv)-2):
    print "loading.. ", sys.argv[fn+2]
    temp = pickle.load(open(sys.argv[fn+2], "rb"))
    triangles.update(temp)
    print "done."
print "done all."

balanced = 0
unbalanced = 0
unique_triangles = {}
type_triangles = {}
for t in triangles:
    if (check_for_self_loops(t)):
        continue
    uniq = get_unique(t)
    if uniq in unique_triangles:
        continue
    unique_triangles[uniq] = True
    tt =  get_sign(G, t)

    typ = tuple(sorted(tt))
    if typ not in type_triangles:
        type_triangles[typ] = 1
    else:
        type_triangles[typ] += 1


for t in sorted(type_triangles.keys()):
    is_balanced = check_for_structural_balance(t)
    print "%s & %s & %s \\" % (t, type_triangles[t], "Sim" if is_balanced else "Não")
    if is_balanced:
        balanced += type_triangles[t]
    else:
        unbalanced += type_triangles[t]

print "Balanced: ", balanced
print "Unbalanced: ", unbalanced
print "Total:", balanced + unbalanced
