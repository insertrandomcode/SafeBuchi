import numpy as np
from typing import Set, Tuple
from parity_game import Game


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
            for dest in list(game.dict[vertex].edges):
                edges.append( (vertex, dest) )
        else:
            edges.append( (vertex, 'losing') )

    return Game(info, edges)

from zielonkas import zielonkas

if __name__ == '__main__':
    # Wikipedia Graph
    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]

    wik_game = Game(zip(range(verts), info), edges)

    sb_game = safe_buchi_game(set([3]), set({4,5,6,7}), 1, wik_game)
    
    print(zielonkas(sb_game))




