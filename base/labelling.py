import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.parity_game import Game
from base.attract import attract_star

from functools import total_ordering
from typing import Set, List, Tuple

@total_ordering
class Label():
    def __init__(self, value: int, player: int, origin:int):
        self.value = value
        self.owner = player
        self.origin = origin
    
    def __str__(self) -> str:
        return f"{self.value}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: "Label") -> bool:
        assert self.owner == other.owner, "Comparing Labels from Different Owners"

        return self.value == other.value
    
    def __lt__(self, other: "Label") -> bool:
        assert self.owner == other.owner, "Comparing Labels from Different Owners"

        # Case where either is negative
        if self.value < 0 or other.value < 0:
            return self.value < other.value

        if self.value % 2 == self.owner:
            if other.value % 2 != self.owner:
                return False
            else:
                return self.value < other.value
        
        else:
            if other.value % 2 == self.owner:
                return True
            else:
                return self.value > other.value
    
# TODO: think of modifying this rather than having an entirely different algorithm
def labelling(G: Game, X: Set[int], player:int, strategy: bool=False) -> dict:
    # Note that this version of the labelling works for j-dominating paths and thus \ell is no longer lower bounded

    def best_label_successor(labels: List[Label], choosing: int) -> Label:
        return Label(-1,player,0) if len(labels) == 0 else ( max(labels) if player == choosing else min(labels) )


    labels = {key: Label(-1, player, key) for key in G.nodes()}
    strat = {key: -1 for key in G.nodes(lambda x : x.owner == player)}

    G_ = G.invert_edges()

    # initial labels
    can_reach = set([])
    for x in X:
        for v in G_[x].edges:
            if G[v].owner == player or G[v].edges.issubset(X):
                can_reach.add(v)

    for v in can_reach:
        labels[v] = best_label_successor(
            [Label(G[x].priority, player, x) for x in G[v].edges.intersection(X)], # by attractor rules this works
            G[v].owner
        )
        if G[v].owner == player:
            strat[v] = labels[v].origin

    updated = True
    while updated:
        updated = False
        # having staggered updates makes the proof of correctness easier
        new_labels = {key: Label(-1, player, key) for key in G.nodes()}

        for v in G.nodes():
            successor_labels = [
                    Label(
                        max(labels[s].value, G[s].priority) if (labels[s].value >= 0 or s in X) else -1, 
                        player, 
                        s
                    ) 
                    for s in G[v].edges
                ]

            new_labels[v] = max(labels[v], best_label_successor(successor_labels, G[v].owner))

            updated_here = labels[v].value != new_labels[v].value
            updated |= updated_here

            if G[v].owner == player and updated_here:
                strat[v] == new_labels[v].origin
        
        labels = new_labels # note that we will never have a non-negative value become negative

    return labels if not strategy else (labels, strat)

def labelling_nostop(G: Game, X: Set[int], player: int, strategy: bool = False) -> dict:
    raise NotImplementedError("Deprecated due to incorrectness -- can loop forever")
        
if __name__ == '__main__':
    # Wikipedia Graph
    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]

    game = Game(zip(range(verts), info), edges)
    print(labelling_nostop(game, set([1]), 0, True))



