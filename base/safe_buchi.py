import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

import numpy as np
from typing import Set, Tuple
from base.parity_game import Game

def safe_buchi_game(target_set: Set[int], exclude_set: Set[int], player: int, game: Game) -> Game:

    # Assertions
    assert target_set.intersection(exclude_set) == set([]), f'{target_set} overlaps with {exclude_set}'
    assert player in [0,1], f'player: {player} not in [0,1]'

    # Extract ownership information from the game

    #initialise game with 'losing' vertex
    info = [('losing', (player, player+1))]
    edges = [('losing', 'losing')]

    for vertex in game.dict.keys():
        # priority is player + 2 if in target set else player + 1, edges not for exclude set

        info.append( (vertex, (game.dict[vertex].owner, player + 1 + (vertex in target_set))) )
        if vertex not in exclude_set:
            for dest in game.dict[vertex].edges:
                edges.append( (vertex, dest) )
        else:
            edges.append( (vertex, 'losing') )

    return Game(info, edges)