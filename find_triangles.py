import re
import networkx as nx
import pickle
import sys
import signal

inputfilename = sys.argv[1]
outputfilename = sys.argv[2]
start = None
end = None
if len(sys.argv) > 3:
    start = int(sys.argv[3])
    if len(sys.argv) > 4:
        end = int(sys.argv[4])


def get_connecting_edge(edges, n1, n2):
    for e in edges:
        if n2 is get_other_node(n1, e):
            return e
    return None

def remove_self_loops(edges):
    res = list(edges)
    for e in edges:
        if e[0] is e[1]:
            res.remove(e)
    return res
def make_triangle_triple(e1, e2, e3):
    return tuple(sorted((e1, e2, e3), lambda a, b: cmp(sorted(a), sorted(b))))
def get_other_node(node, edge):
    return edge[(list(edge).index(node)+1) % 2]
def get_edges(node):
    return sorted(list(G.in_edges([node], data=True) + G.out_edges([node], data=True)), lambda a, b : get_other_node(node, a) - get_other_node(node, b))
def get_all_neighbors(node):
    return set([get_other_node(node, x) for x in get_edges(node)])
def get_triangles(node):
    neighbors = remove_self_loops(get_edges(node))
    triangles = []
    print neighbors
    for n1 in neighbors:
        for n2 in neighbors[neighbors.index(n1)+1:]:
            if get_other_node(node, n2) in nx.all_neighbors(G, get_other_node(node, n1)):
                n2_neighbors = get_edges(get_other_node(node, n2))
                n1_edge = get_connecting_edge(n2_neighbors, get_other_node(node, n2), get_other_node(node, n1))
                if n1_edge is not None:
                    triangles.append(make_triangle_triple(n1, n2, n1_edge))
                
    return triangles

def edge_exists(G, n1, n2):
    return n1 in G[n2] or n2 in G[n1]
def get_edge(G, n1, n2):
    if n1 in G[n2]:
        return (n2, n1)
    else:
        return (n1, n2)
def enrich_edge(G, edge):
    return (edge[0], edge[1], G[edge[0]][edge[1]])

def save_all(triangles, final_index):
    pickle.dump(triangles, open(outputfilename + "_%d_%d.pickle" % (start, final_index if final_index is not None else end), "wb"))

def get_all_triangles(G, start, end):
    triangles = {}
    index = start

    def signal_handler(signal, frame):
            print('Saving... ' + str(index))
            save_all(triangles, index)
            sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


    print "total size ", len(G.edges())
    for edge in G.edges()[start:end]:
        if index % 300 == 0:
            print "t", edge, index
        index += 1
        for node in G.nodes():
            if edge_exists(G, edge[0], node) and edge_exists(G, edge[1], node):
                t = make_triangle_triple(edge, get_edge(G, edge[0], node), get_edge(G, edge[1], node))
                if t not in triangles:
                    triangles[t] = True
    return triangles



G = nx.DiGraph()
#G.add_edge(1,2, weight=-1)
#G.add_edge(3,2, weight=1)
#G.add_edge(1,3, weight=1)
#G.add_edge(3,4, weight=-1)
#G.add_edge(4,2, weight=-1)
#G.add_edge(10,11, weight=-1)
#G.add_edge(10,12, weight=1)
#G.add_edge(12,11, weight=-1)


p = re.compile("([0-9]+)[ \t]+([0-9]+)[ \t]+([-+0-9]+).*")
with open(inputfilename) as f:
    for line in f:
        if line[0] == "#":
            continue
        
        m = p.match(line)
        G.add_edge(int(m.group(1)), int(m.group(2)), weight=int(m.group(3)))

triangles =  get_all_triangles(G, start, end)
save_all(triangles, None)

#triangle_types = {}
#for t in triangles:
#    tt =  tuple(zip(get_category(t), get_sign(G, t)))
#    print tt, check_for_status_balance(tt)
#
#print triangle_types
