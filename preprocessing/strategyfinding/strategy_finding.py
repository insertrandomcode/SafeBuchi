import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.parity_game import Game
from base.labelling import labelling, Label
from base.weighted_graph import WGraph

from typing import Set


def auxiliary_graph(G: Game, X: Set[int], player: int) -> "WGraph":

    Vertices = X
    Arcs = set([])
    
    for x in X:
        # generating "best" paths from every vertex in X to every other vertex in X

        labels = { v: Label(-1, player, v) for v in G.nodes() }
        for s in G[x].edges:
            labels[s].value = max(G[s].priority, G[x].priority)

        for _ in range(len(G)):
            updated = False
            
            for v in [key for key in labels.keys() if labels[key].value >= 0 and key not in X]:
                for s in G[v].edges:
                    target_label = Label(max(G[s].priority, labels[v].value), player, v)

                    if target_label > labels[s]:
                        labels[s] = target_label
                        updated = True
            
            if not updated:
                break
        
        for x2 in X:
            if labels[x2].value >= 0:
                Arcs.add((x, x2, labels[x2].value))
    
    return WGraph(Vertices, Arcs)

def strategy_graph(G: Game, strategy: dict, player: int) -> "Game":
    assert all([strategy[v] in G[v].edges or strategy[v] == -1 for v in strategy.keys()]), "Strategy is inconcsistent with game"
    assert strategy.keys() == G.nodes(lambda x : x.owner == player), "Strategy is not complete"

    # set the edges to be consistent with the strategy
    G_ = G.copy()
    G_.edges = set([(src, dst) for src, dst in G.edges if G[src].owner == 1-player])

    for v in strategy.keys():
        if strategy[v] == -1:
            G_[v].edges = set([list(G_[v].edges)[0]]) # `random' selection
            G_.edges.add((v, list(G_[v].edges)[0]))
        else:
            G_[v].edges = set([strategy[v]])
            G_.edges.add((v,strategy[v]))

    return G_

if __name__ == '__main__':
    # Wikipedia Graph
    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]

    wik_game = Game(zip(range(verts), info), edges)

    ## set this to whatever maze to get results
    player = 0
    X = set([1, 7])
    
    labels, strat = labelling(wik_game, X, player, True)

    G_s = strategy_graph(wik_game, strat, player)
    
    G_s.visualise("wik_strat.png")

    WG = auxiliary_graph(G_s, X, 1-player)

    WG.visualise("wik_aux.png")
