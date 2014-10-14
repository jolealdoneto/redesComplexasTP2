import sys
import pickle

f = open(sys.argv[1], "rb")

triangles = pickle.load(f)
print triangles
