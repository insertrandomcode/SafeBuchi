import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.parity_game import Game
from algorithms.zielonkas import attract
from base.labelling import labelling
from preprocessing.preprocessor import Preprocessor

from typing import Set

class WinningCorePreprocessor(Preprocessor):

    def preprocess(self, G: Game) -> "Stuff":

        partition = winning_core_underapproximation(G)

        return G.exclude(partition[0]).exclude(partition[1]), partition

def winning_core_underapproximation(G: Game) -> (Set[int], Set[int]):
    # start with whole set X
    for player in [0, 1]:
        X = G.nodes()

        for i in range(len(G)):
            labels = labelling(G, X, player)

            next_ = [x for x in X if labels[x].value>=0 and labels[x].value % 2 == player]

            if X == next_:
                break

            X = next_
        
        if len(X) > 0:

            A = attract(G, player, X)

            W0, W1 = winning_core_underapproximation(G.exclude(A))

            return ( W0.union(A), W1 ) if player == 0 else ( W0, W1.union(A) )
    
    return ( set([]), set([]) )

if __name__ == '__main__':
    # Wikipedia Graph
    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]

    wik_game = Game(zip(range(verts), info), edges)
    print( winning_core_underapproximation(wik_game) )