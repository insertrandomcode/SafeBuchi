import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Set, List, Tuple

from base.parity_game import Game
from preprocessing.preprocessor import Preprocessor
from base.labelling import labelling
from base.attract import attract

# NOTE: almost identical to winning_core_underestimation

class TrapFindingPreprocessor(Preprocessor):

    def preprocess(self, G: Game) -> Tuple[Game, Tuple[Set, Set]]:
        
        partition = trap_finding_underapproximation(G)

        return G.exclude(partition[0]).exclude(partition[1]), partition


def trap_finding_underapproximation(G: Game) -> Tuple[Set, Set]:

    for player in [0,1]:

        X = G.nodes(lambda x : x.owner == 1-player)

        for _ in range(len(G.nodes())):

            labels = labelling(G, X, player)

            next_ = set([x for x in X if labels[x].value >= 0 and labels[x].value % 2 == player])

            if X == next_:
                break
        
            X = next_
                
        if len(X) > 0:
            A = attract(G, player, X)

            W0, W1 = trap_finding_underapproximation(G.exclude(A))

            return ( W0.union(A), W1 ) if player == 0 else ( W0, W1.union(A) )
    
    return ( set([]), set([]) )



