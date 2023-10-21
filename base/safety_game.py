import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.parity_game import Game
from base.safe_buchi import safe_buchi_game
from typing import Set

def safety_game(G: Game, target_set: Set[int], exclude_set: Set[int], player: int) -> Game:
    # assert max_priority >= player, "max prio less than player -- if this is a problem look into it"

    # Make 'win' from each of the target set, remove all other outgoing edges from the target set
    G_ = G.copy()
    G_.dict['win'] = Game.Node(player, player, set(['win']))

    for node in G.nodes():
        if node in target_set:
            G_[node].edges = set(['win'])
    
    return safe_buchi_game(set(['win']), exclude_set, player, G_)