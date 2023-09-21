import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Tuple, Set

from base.parity_game import Game
from preprocessing.strategyfinding.strategy_finding import strategy_graph
from preprocessing.safebuchi_preprocessing import fatal_attractor_preprocessor
from preprocessing.preprocessor import Preprocessor
from base.labelling import labelling, Label, labelling_nostop
from base.attract import attract, safe_attract_star

# NOTE: this is just exactly trapfinding -- finds nothing else (proof in overleaf)

class StaggeredTrapPreprocessor(Preprocessor):

    def preprocess(self, G: Game):
        partition = staggered_trap_underestimation(G)

        return G.exclude(partition[0]).exclude(partition[1]), partition

def staggered_trap_underestimation(G: Game) -> Tuple[Set[int], Set[int]]:
    # Can't solve games that labelling strategy finding can -- what's it getting wrong?

    if len(G) == 0:
        return set([]), set([])

    for player in [0,1]:

        X = G.nodes(lambda x : x.owner == 1-player)

        for _ in range(len(X)):
            # Get initial labels for reachable
            X, labels, strat = label_until_condition(G, X, player, lambda x : x.value >= 0)

            good_X = set([x for x in X if labels[x].value % 2 == player])

            for p in set([labels[x].value for x in good_X]):

                good_X_p = set([x for x in good_X if labels[x].value >= p])
                labels_, strat = labelling(G, good_X_p, player, True)

                X_p = good_X_p.union(set([x for x in X if labels_[x].value >= 0 and (
                    labels_[x].value % 2 == player or
                    labels_[x].value <= p
                )]))

                labels_, strat = labelling(G, X_p, player, True)

                if len(X_p) > 0 and all([labels_[x].value >= p and labels_[x].value % 2 == player for x in good_X_p]):
                    # should be winning here (all x in X_p) can either get back to X_p with winning path
                    # or can get to a vertex that has a path back to X_p with a winning path at most p - with a path at least p

                        A = attract(G, player, X_p)

                        W0, W1 = staggered_trap_underestimation(G.exclude(A))

                        return ( W0.union(A), W1 ) if player == 0 else ( W0, W1.union(A) )
    
    return set([]), set([])

def label_until_condition(G: Game, X: Set[int], player: int, condition: "Callable[Label, Bool]"):

    labels, strat = labelling(G, X, player, True)

    while not all([condition(labels[x]) for x in X]):
        X = [x for x in X if condition(labels[x])]

        labels, strat = labelling(G, X, player, True)
    
    return X, labels, strat