import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Tuple, Set
import numpy as np
from base.parity_game import Game
from base.attract import attract

def zielonkas(G: Game) -> Tuple[Set[int], Set[int]]:
    p = G.max_priority()

    if p == 0:
        return G.nodes(), set([])
    
    else:
        U = G.nodes(lambda x : x.priority == p)
        i = p % 2
        A = attract(G, i, U)

        W_0, W_1 = zielonkas(G.exclude(A))

        if (W_1 if i == 0 else W_0) == set([]):
            return ( G.nodes(), set([]) ) if i == 0 else (set([]), G.nodes())
        
        B = attract(G, 1-i, W_1 if i == 0 else W_0)

        W__0, W__1 = zielonkas(G.exclude(B))

        return ( W__0, W__1.union(B) ) if i == 0 else ( W__0.union(B), W__1 )

if __name__ == '__main__':
    pass
    # Wikipedia Graph
    # verts = 8
    # info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    # edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
    #          (5,7), (6,1), (6,7), (7,2), (7, 5)]

    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]

    # ParityToSat Graph
    # verts = [0,1,2,3,4,5,6,7]
    # info = [(0, 2), (1, 3), (0, 1), (1, 0), (1, 4), (1, 1), (0, 4), (0, 2)]
    # info = list(map(lambda x : (x[0], 8-x[1]), info))
    # edges = [
    #         (0,1), (0, 4), 
    #         (1,0), (1,2), 
    #         (2,3) ,(2,6) , 
    #         (3, 3), (3, 1), 
    #         (4, 6), (4, 5), 
    #         (5, 4), (5, 6),
    #         (6, 5), (6, 7),
    #         (7, 4)]

    G = Game(zip(range(verts), info), edges)
    W0, W1 = zielonkas(G)

    print(W0, W1)