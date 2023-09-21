import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.parity_game import Game
from base.labelling import labelling, Label

from base.tarjan_scc import tarjan_scc, tarjan_scc_wg

from preprocessing.strategyfinding.strategy_preprocessor import losing_edges
from preprocessing.strategyfinding.strategy_finding import strategy_graph, auxiliary_graph

# TODO: optimise code -- make cleaner

def full_cover_layering(G: Game, player: int):

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

    G_a = auxiliary_graph(G_s, X, 1-player)

    # remove the max vertex cover from the game and find SCCs
    L = losing_edges(G_a, player)

    LV = set([src for src, dst, val in L]).union(set([dst for src,dst,val in L]))

    G_x = G_a.exclude(LV)

    G_x.visualise('fail_game_aux_excl.png')

    SCCs = tarjan_scc_wg(G_x)

    G_SCC = G.copy()

    next_ = max(G.nodes()) + 1

    # replace SCCs with DAG
    for SCC in SCCs:

        if len(SCC) <= 1:
            continue

        outgoing_v = set([])

        for v in SCC:
            G_SCC[v].edges = set([])
            G_SCC[v].priority = 0

            for w, _ in G_a.edges[v]:
                if w not in SCC:
                    outgoing_v.add(w)

        for dst in outgoing_v:
            # for every vertex in SCC, find worst path to outgoing_v
            paths = G_a.best_paths(dst, 1-player)

            # replace path to that vertex with dummy to that arc with 'middle' vertex wi
            for src in SCC:
                if paths[src].value < 0: # shouldn't ever happen
                    continue

                G_SCC.dict[next_] = Game.Node(player, paths[src].value, set([dst]))
                G_SCC[src].edges.add(next_)
                next_ += 1
    
    return G_SCC






    