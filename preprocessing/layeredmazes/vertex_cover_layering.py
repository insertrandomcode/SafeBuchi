import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.parity_game import Game
from base.labelling import labelling, Label
from base.attract import safe_attract_star

from base.tarjan_scc import tarjan_scc, tarjan_scc_wg
from base.weighted_graph import WGraph

from preprocessing.strategyfinding.strategy_finding import strategy_graph

from typing import Set

# TODO: optimise code -- make cleaner

def vertex_cover_layering(G: Game, player: int):

    # Get strategy graph for G
    X = G.nodes(lambda x : x.owner == 1-player)

    for _ in range(len(G.nodes())):

        labels = labelling(G, X, player)

        next_ = set([x for x in X if labels[x].value >= 0])

        if X == next_:
            break
    
        X = next_
    
    labels, strategy = labelling(G, X, player, True)

    G_s = strategy_graph(G, strategy, player)

    L = winning_vertices(G_s, 1-player)

    # assert len(L) > 0, 'game is not losing for player under `best` strategy'
    
    SCCs = tarjan_scc(G_s.exclude(L))

    # G.visualise('game_L.png', L)

    G_SCC = G.copy()
    next_ = max(G.nodes()) + 1

    for SCC in SCCs:

        if len(SCC) <= 1:
            continue
        
        # restricted 1 player game to the SCC
        G_r = Game(
            set([
                (v, (G_s[v].owner, G_s[v].priority))
                for v in G_s.nodes()
            ]),
            set([
                (src, dst)
                for src,dst in G_s.edges
                if src in SCC
            ])
        )

        # find outgoing edges of SCC

        outgoing_v = set([])

        # TODO: technically we assume the SCC is not a dominion which may be false and we get errors in these. 
        #   But such dominions are preprocessable by previous methods so we can ignore them

        for v in SCC:
            G_SCC[v].edges = set([])
            G_SCC[v].owner = 1-player # indicates how the losing player is in control
            G_SCC[v].priority = 0

            outgoing_v = outgoing_v.union(G[v].edges.difference(SCC))

        # find best path through SCC 
        for dst in outgoing_v:    

            labels = labelling(G_r, set([dst]), 1-player)
            labels_inv = {}

            # 1 new vertex per unique prio path to each dst -- somewhat reduces clutter
            for val in set([labels[src].value for src in SCC]):
                G_SCC.dict[next_] = Game.Node(player, val, set([dst]))
                labels_inv[val] = next_

                next_ += 1

            for src in SCC:
                if labels[src].value < 0: # shouldn't ever happen -- but does due to assumptions
                    continue

                G_SCC[src].edges.add( labels_inv[labels[src].value] )
    
    return G_SCC
    

def winning_vertices(G: Game, player: int) -> Set[int]:
    # return vertices in solitaire game G that are winning for player

    winning = set([])

    vertices_of_interest = G.nodes(lambda x : x.priority % 2  == player)

    for v in vertices_of_interest:
        if v in safe_attract_star(G, set([v]), player, lambda x : x.priority <= G[v].priority):
            winning.add(v)

     # return this set
    return winning

