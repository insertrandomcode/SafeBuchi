import sys
import os

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Tuple, Set, List
from itertools import product

from base.parity_game import Game
from base.tarjan_scc import tarjan_scc
from preprocessing.strategyfinding.strategy_finding import strategy_graph
from preprocessing.safebuchi_preprocessing import fatal_attractor_preprocessor
from preprocessing.preprocessor import Preprocessor
from base.labelling import labelling, Label
from base.attract import attract, safe_attract_star

import time

class TangleTrapPreprocessor(Preprocessor):

    def preprocess(self, G: Game):
        partition = tangle_trap_underestimation(G)

        return G.exclude(partition[0]).exclude(partition[1]), partition

def tangle_trap_underestimation(G: Game, debug=False, iter=0) -> Tuple[Set[int], Set[int]]:
    if len(G) == 0:
        return set([]), set([])
        
    for player in [0,1]:
        if player == 1: iter += 1

        if debug: 
            if not os.path.exists(f"z_game_debug"): os.mkdir("z_game_debug")
            if not os.path.exists(f"z_game_debug\\iter{iter}"): os.mkdir(f"z_game_debug\\iter{iter}")

        # Do 'best priority' strat underestimation 

        _, strat = labelling(G, G.nodes(), player, True)

        one_player = strategy_graph(G, strat, player)

        # find looping vertices for opponent in 1 player game

        losing = loop_vertices(one_player, 1-player)

        # early exit to avoid costly tangle labelling
        if len(losing) == 0:
            return (G.nodes(), set([])) if player == 0 else (set([]), G.nodes())

        # Do the scc decomposition of the one player game
        tangles = [scc for scc in tarjan_scc(one_player.exclude(losing)) if 
            len(scc) > 1 or scc.issubset(G[next(iter(scc))].edges)]
        in_tangle, tangle_edges = get_tangle_accessories(G, tangles, player)

        if debug:
            print(iter, 'tangles', tangles)
            for i in range(len(tangles)):
                G.visualise(f'z_game_debug\\iter{iter}\\tangle{i}.png', subset=tangles[i])

        # early exit to avoid costly tangle labelling -- tangles with no outgoing edges (for 1-j) are domains of j
        if any([len(tangle_edges[i]) == 0 for i in range(len(tangles))]):
            X = set([])

            for i in range(len(tangles)):
                if len(tangle_edges[i]) == 0: X = X.union(tangles[i])
        else:
            # do the tagle labelling, this time picking 'good values'
            X = G.nodes()
            labels = {v:Label(-1,0,0) for v in G.nodes()}

            for i in range(len(G)):
                if debug:
                    print(iter, i, X)
                    G.visualise(f'z_game_debug\\iter{iter}\\step{i}.png', subset=X)
                
                labels = tangle_labelling(G, X, player, tangles, in_tangle, tangle_edges)

                if all([labels[x].value >= 0 and labels[x].value % 2 == player for x in X]):
                    break
                    
                X = [x for x in X if labels[x].value >= 0 and labels[x].value % 2 == player]

            # we now have a trap where the options for non-trapping was to stay in a 

            # #raise ValueError

        if len(X) > 0:
            # should be winning here (all x in X_p) can either get back to X_p with winning path
            # or can get to a vertex that has a path back to X_p with a winning path at most p - with a path at least p

            A = tangle_attract(G, X, player, tangles, in_tangle, tangle_edges)

            if debug: print(player, X, labels)

            G_ = G.exclude(A)

            W0, W1 = tangle_trap_underestimation(G.exclude(A), debug=debug, iter=iter+1)

            return ( W0.union(A), W1 ) if player == 0 else ( W0, W1.union(A) )
    
    return set([]), set([])    

def get_tangle_accessories(G, tangles, player):
    in_tangle = {v: [i for i in range(len(tangles)) if v in tangles[i]] for v in G.nodes()}
    tangle_edges = [set([]) for _ in range(len(tangles))]

    for i in range(len(tangles)):
        for v in tangles[i]:
            if G[v].owner == 1-player:
                tangle_edges[i] = tangle_edges[i].union(G[v].edges.difference(tangles[i]))

    return in_tangle, tangle_edges

def tangle_attract(G, U, player, tangles, in_tangle, tangle_edges, give_updated = False):

    attractor = set(U)

    G_ = G.invert_edges()

    # remove internal edges
    for u in attractor:
        G_[u].edges = G_[u].edges.difference(attractor)

    added = U

    while len(added) != 0:

        to_add = set([])

        for v in added:
            for e in G_[v].edges:
                # sacrifices speed for legibility
                if (G[e].owner == player or G[e].edges.issubset(attractor) or
                    any([tangle_edges[i].issubset(attractor) for i in in_tangle[e]])):
                    to_add.add(e)

        attractor = attractor.union(to_add)
        added = to_add

        #remove internal edges again
        for v in to_add:
            G_[v].edges = G_[v].edges.difference(attractor)
                
    return (attractor, attractor != U) if give_updated else attractor

def tangle_labelling(G: Game, X: Set[int], player: int, tangles, in_tangle, tangle_edges) -> dict:
    # Seems super duper slow when nontrivial tangles are introduced -- maybe go back to stop-labelling

    # these tangles are all disjoint TODO: maybe modify this to work for overlapping tangles
    # NOTE: all tangle_labelled values should have len(tangle_edges[i]) > 0 and in front
    #       this does not affect anything when excluded as if it has no edges is losing for that player anyway

    tangle_labelled = [tangle_edges[i].issubset(X) for i in range(len(tangles))]

    def best_label_successor(labels: List[Label], choosing: int) -> Label:
        return Label(-1, player, 0) if len(labels) == 0 else (max(labels) if player == choosing else min(labels))

    labels = {key: Label(-1, player, key) for key in G.nodes()}

    G_ = G.invert_edges()

    # initial labels
    can_reach = set([])
    for x in X:
        for v in G_[x].edges:
            if G[v].owner == player or G[v].edges.issubset(X) or any([tangle_labelled[i] for i in in_tangle[v]]):
                can_reach.add(v)

    for v in can_reach:
        labels[v] = best_label_successor(
            [Label(G[x].priority, player, x) for x in G[v].edges.intersection(X)], # by tangle attractor rules this works
            G[v].owner
        )

    labelled = set([v for v in G.nodes() if labels[v].value >= 0])
    tangle_labelled = [tangle_edges[i].issubset(labelled) for i in range(len(tangles))]

    updated = True
    i = 0
    while updated:
        # print(f'------------ {i} --------------')
        # print(labels)
        # print(tangle_labelled)
        if i > len(G):
            raise ValueError("Labels Took Longer than Theoretically Maximum")

        i += 1
        updated = False

        # having staggered updates makes the proof of correctness easier
        new_labels = {key: Label(-1, player, key) for key in G.nodes()}

        for v in G.nodes():

            # if v is eligible to ignore -1's due to a tangle
            # NOTE: could be underestimate value if we select label that stays in Tangle
            #   i.e. if we are looping within a tangle to get lower 0
            #   e.g. in the example we can ask 'can we return with 12 or lose' and we can but labelling doesn't find it
            #       because labelling says we reach X earlier and then get stuck in X
            #   If we can encode whether we the label stays inside a tangle - we could pick the best label from successors not
            #       in the tangles. 
            # tangle_bool = G[v].owner == 1-player and any([tangle_labelled[i] for i in in_tangle[v]])

            successor_labels = [
                    Label(
                        max(labels[s].value, G[s].priority) if (labels[s].value >= 0 or s in X) else -1, 
                        player, 
                        s
                    ) 
                    for s in G[v].edges if not ( # stops 1-j from avoiding X by staying in a tangle
                        G[v].owner == 1-player and
                        labels[s].value == -1 and
                        any([s in tangles[i] and tangle_labelled[i] for i in in_tangle[s]])
                    )
            ]

            new_labels[v] = best_label_successor(successor_labels, G[v].owner)

            updated_here = labels[v].value != new_labels[v].value
            updated |= updated_here

            if not updated_here:
                new_labels[v] = labels[v]

            if new_labels[v].value >= 0:
                labelled.add(v)

        labels = new_labels # note that we will never have a non-negative value become negative
        tangle_labelled = [tangle_edges[i].issubset(labelled) for i in range(len(tangles))]

        if not updated:
            break
    return labels

def loop_vertices(G: Game, player: int):

    priorities = set([G[v].priority for v in G.nodes(lambda x : x.priority % 2 == player)])
        
    winning_vertices = set([])

    for p in priorities:
        player_ = p % 2
        loop_vertices = G.nodes(lambda x : x.priority == p)

        for _ in range(len(G)):
            prev = len(loop_vertices)

            loop_vertices = loop_vertices.intersection(safe_attract_star(G, player_, loop_vertices, lambda x : x.priority <= p))

            if prev == len(loop_vertices) or len(loop_vertices) == 0:
                break
        
        winning_vertices = winning_vertices.union(loop_vertices)
    
    return winning_vertices
