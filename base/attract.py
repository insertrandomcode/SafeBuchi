import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Tuple, Set
import numpy as np
from base.parity_game import Game

def safe_attract(G: Game, i: int, U: Set[int], inc_cond: "Callable[int, bool]") -> Set[int]:
    # attractor with conditions on visible vertices
    assert all(inc_cond(G[u]) for u in U), 'attract set U does not meet inclusion condition'

    if len(U) == 0:
        return U
    
    G_ = G.invert_edges()

    attractor = set(U)
    added = U

    while len(added) != 0:
        to_add = set([])

        for node in added:

            # for each incoming edge into the node
            for edge in G_[node].edges:
                # either can force because owner, or can force because only option
                if inc_cond(G[edge]) and ( G_[edge].owner == i or G[edge].edges.issubset(attractor) ):
                    to_add.add(edge)

        attractor = attractor.union(to_add)
        added = to_add

        #remove internal edges again
        for node in to_add:
            G_[node].edges = G_[node].edges.difference(attractor)
                
    return attractor

def safe_attract_star(G: Game, i: int, U: Set[int], inc_cond: "Callable[int, bool]"):
    # vertices forcibly 1 step away
    X = G.nodes(lambda x :
            inc_cond(x) and ( 
                (x.owner == i and len(x.edges.intersection(U)) > 0) or 
                (x.owner == 1-i and x.edges.issubset(U))
            )
        )

    return safe_attract(G, i, X, inc_cond)

def attract(G: Game, i: int, U: Set[int]):
    return safe_attract(G, i, U, lambda x : True)

def attract_star(G: Game, i:int, U: Set[int]):
    return safe_attract_star(G, i, U, lambda x : True)

if __name__ == '__main__':
    # testing correctness of safe_attract_star

    G = Game(zip(range(3), [(0, 1), (0, 3), (0, 4)]), [(0,1), (1,2), (2,0)])
    G.visualise('simple_ex.png', subset=safe_attract_star(G, [1], 0, lambda x : x.priority <= 3))
    