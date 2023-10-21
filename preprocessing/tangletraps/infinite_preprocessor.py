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
from base.labelling import labelling, Label
from base.attract import attract, safe_attract_star

class InfiniteMaxLabelPreprocessor(Preprocessor):

    def preprocess(self, G: Game):
        partition = infinite_label_underestimation(G)

        return G.exclude(partition[0]).exclude(partition[1]), partition

def infinite_label_underestimation(G: Game) -> Tuple[Set[int], Set[int]]:
    # Can't solve games that labelling strategy finding can -- what's it getting wrong?

    if len(G) == 0:
        return set([]), set([])

    for player in [0,1]:

        labels, strat = find_infinite_label(G, G.nodes(), player, True)

        one_player_G = strategy_graph(G, strat, player)

        winning = G.nodes().difference( fatal_attractor_preprocessor(one_player_G, 1-player)[1-player] )
    
        if len(winning) > 0:
            # print(winning, player)

            A = attract(G, player, winning)

            W0, W1 = infinite_label_underestimation(G.exclude(A))

            return ( W0.union(A), W1 ) if player == 0 else ( W0, W1.union(A) )
    
    return set([]), set([])

# TODO: this doesn't work for some games
# this reduces the priorities to forced loops of value + or minimum values in the game.
# doing so step by step by cause problems -- i.e. in infinitely-often-read-write it will have labels of all 1 eventually 
#   - which is nonsene
def find_infinite_label(G: Game, X: Set[int], player:int, strategy = False) -> dict:
    labelling_method = labelling

    G_ = G.copy()
    labels, strat = labelling_method(G_, X, player, True)

    for _ in range(len(G)): # TODO: think of reducing this maxiter
        updated = False

        for v in X:
            successors = [Label(labels[e].value, player, e) for e in G[v].edges]
            best_successor = max(successors) if G[v].owner == player else min(successors)

            # CASE 1: -1 -- shouldn't happen -- can't with current next_ choice
            # CASE 2: > self - can't happen (due to labels update)
            # CASE 3: = self - means we reach some other $x \in X$ with priority ell_v so we're fine
            # CASE 4: < self - means we never reach priority ell_v again - so update
            updated = updated or (best_successor.value < G_[v].priority)
            G_[v].priority = min(best_successor.value, G_[v].priority)

        if not updated:
            break
            
        labels, strat = labelling_method(G_, X, player, True)

    return labels if (not strategy) else (labels, strat)