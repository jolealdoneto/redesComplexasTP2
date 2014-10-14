import pickle
import networkx as nx

G = nx.DiGraph()

p = re.compile("([0-9]+)[ \t]+([0-9]+)[ \t]+([-+0-9]+).*")
with open("soc-sign-epinions.txt") as f:
    for line in f:
        if line[0] == "#":
            continue
        
        m = p.match(line)
        G.add_edge(int(m.group(1)), int(m.group(2)), weight=int(m.group(3)))

def get_category(triangle):
    return tuple(map(lambda e: "1" if min(e) is e[0] else "0", triangle))
def get_sign(G, triangle):
    return tuple(map(lambda e: G[e[0]][e[1]]['weight'], triangle))

triangle_types = {}
for t in triangles:
    tt =  tuple(zip(get_category(t), get_sign(G, t)))
    if tt in triangle_types:
        triangle_types[tt] += 1
    else:
        triangle_types[tt] = 1

print triangle_types
