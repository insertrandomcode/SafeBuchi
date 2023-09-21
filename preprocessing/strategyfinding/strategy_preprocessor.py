import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Tuple, Set

from base.parity_game import Game
from preprocessing.strategyfinding.strategy_finding import strategy_graph, auxiliary_graph, WGraph
from preprocessing.preprocessor import Preprocessor
from base.labelling import labelling
from base.attract import attract

class StrategyFindingPreprocessor(Preprocessor):

    def preprocess(self, G: Game):
        partition = strategy_underestimation(G)

        return G.exclude(partition[0]).exclude(partition[1]), partition

def strategy_underestimation(G: Game) -> Tuple[Set[int], Set[int]]:
    for player in [0,1]:

        X = G.nodes(lambda x : x.owner == 1-player)

        for _ in range(len(G.nodes())):

            labels = labelling(G, X, player)

            next_ = set([x for x in X if labels[x].value >= 0])

            if X == next_:
                break
        
            X = next_
    
        ## TODO: prove that if len == 0 means the whole game is winning for the other player
        if len(X) > 0:
            
            labels, strategy = labelling(G, X, player, True)

            G_s = strategy_graph(G, strategy, player)

            G_a = auxiliary_graph(G_s, X, 1-player)

            if len( losing_edges(G_a, player) ) == 0: #TODO: edit to be component specific
                A = attract(G, player, X)

                W0, W1 = strategy_underestimation(G.exclude(A))

                return ( W0.union(A), W1 ) if player == 0 else ( W0, W1.union(A) )
    
    return set([]), set([])
        

def losing_edges(WG: WGraph, player: int) -> bool:

    danger_edges = {src: [(dst, val) for (dst,val) in WG.edges[src] if val % 2 == 1-player] for src in WG.edges.keys()}
    losing_edges = set([])

    for src in WG.verts:
        for dst, val in danger_edges[src]:

            if WG.reachable(dst, src, lambda x: x[2] <= val):
                losing_edges.add((src,dst,val))
                # return False # can return to edge without reaching vertex with edge as great
    
    return losing_edges

