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

def get_category(triangle):
    return tuple(map(lambda e: 1 if min(e) is e[0] else 0, triangle))
def get_sign(G, triangle):
    return tuple(map(lambda e: G[e[0]][e[1]]['weight'], triangle))
def check_for_status_balance(signed_triangle):
    comp = { 'a': 0, 'b': 0, 'c': 0 }
    participating_letters = [['a', 'b'], ['c','a'], ['b', 'c']]

    for aresta, i in zip(signed_triangle, range(len(signed_triangle))):
        letters = participating_letters[i]
        comp[letters[aresta[0]]] += aresta[1]
        comp[letters[(aresta[0] + 1) % 2]] += aresta[1] * -1

    return comp['a'] != comp['b'] and comp['b'] != comp['c'] and comp['a'] != comp['c']

def check_for_self_loops(triangle):
    return len(set(reduce(lambda acc, x: acc + x, triangle))) is not 3
def get_unique(triangle):
    return tuple(sorted(set(reduce(lambda acc, x: acc + x, triangle))))
def rotate(t, n):
    return t[n:] + t[:n]
def flip_all(t):
    return tuple(map(lambda ds: (0, ds[1]) if ds[0] == 1 else (1, ds[1]), t))

def get_sum_direction(t):
    return sum(map(lambda ds: ds[0], t))
def get_canonical(t):
    if get_sum_direction(t) <= 1:
        t = flip_all(t)
    while t[0][0] != 1 or t[1][0] != 1:
        t = rotate(t, -1)
    if (get_sum_direction(t) == 3):
        t = tuple(sorted(t))

    return t

triangles = {}
for fn in range(len(sys.argv)-2):
    print "loading.. ", sys.argv[fn+2]
    temp = pickle.load(open(sys.argv[fn+2], "rb"))
    triangles.update(temp)
    print "done."

print "done all."

unique_triangles = {}
triangle_types = {}
for t in triangles:
    if (check_for_self_loops(t)):
        continue
    uniq = get_unique(t)
    if uniq in unique_triangles:
        continue
    unique_triangles[uniq] = True

    tt =  get_canonical(tuple(zip(get_category(t), get_sign(G, t))))
    if tt in triangle_types:
        triangle_types[tt] += 1
    else:
        triangle_types[tt] = 1

table_s = """
  \\begin{table}[H]
    \caption{%s}
  \centering
  \\begin{tabular}{l c r c}
  \hline\hline
  Índice & Triangulo & Incidências & Balanceado \\\\ [0.5ex]
  \hline
""" % sys.argv[1]

print table_s

balanced = 0
unbalanced = 0
index = 1
for t in sorted(triangle_types.keys()):
    is_balanced = check_for_status_balance(t)
    print "%d & %s & %s & %s \\\\" % (index, t, triangle_types[t], "Sim" if is_balanced else "Não")
    if is_balanced:
        balanced += triangle_types[t]
    else:
        unbalanced += triangle_types[t]
    index += 1
total = balanced + unbalanced

footer_s = """
  \hline
  \hline
  & & \\\\
  Balanceados & %d & %.2f\\%% \\\\
  Desbalanceados & %d & %.2f\\%% \\\\
  \\textbf{Total} & %d & \\\\
  \end{tabular}
  \end{table}
""" % (balanced, float(balanced)/total * 100, unbalanced, float(unbalanced)/total * 100, total)
print footer_s
