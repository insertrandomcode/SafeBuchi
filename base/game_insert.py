import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

import numpy as np

from typing import Set, Tuple, List, Callable
from base.parity_game import Game

def insert_game_into_vertices(
    target_game: Game, 
    insert_game: Game, 
    target_vertices: Set[int],
    qualifier: Callable[Game.Node, bool] = lambda x : True,
    seed: int = None
):
    assert target_game.nodes().issuperset(target_vertices), f"target vertices to replace ({target_vertices}) are not a subset of target game"

    rng = np.random.RandomState(seed)
    acceptable_vertices = list(insert_game.nodes(qualifier))

    target_game_inv = target_game.invert_edges()

    G = target_game.copy()

    for v in target_vertices:
        # incoming is edges to v
        incoming_vertices = rng.choice(acceptable_vertices, len(target_game_inv[v].edges), replace=True)

        # outgoing is edges from v
        outgoing_vertices = rng.choice(acceptable_vertices, len(target_game[v].edges), replace=True)

        # print(f"{v}: iv; {incoming_vertices}, ov; {outgoing_vertices}")

        G = insert_game_into_vertex(G, insert_game, v, incoming_vertices, outgoing_vertices)

    return G

def insert_game_into_vertex(
    target_game: Game,
    insert_game: Game,
    target_vertex: int,
    incoming_vertices: List[int] = [], 
    outgoing_vertices: List[int] = [],
):
    G = target_game.copy()
    ig_verts = list(insert_game.nodes())

    n = max(G.nodes()) + 1

    mapping = {ig_verts[i]: n + i for i in range(len(ig_verts))}

    for v in ig_verts:
        G.dict[mapping[v]] = Game.Node(insert_game[v].owner, insert_game[v].priority, set([mapping[w] for w in insert_game[v].edges]))

    # not a very clean way of doing this but it works
    in_i, out_i = 0, 0

    # incoming vertex handling
    for v in target_game.nodes():
        if target_vertex in target_game[v].edges:
            G[v].edges.remove(target_vertex)
            G[v].edges.add( mapping[ incoming_vertices[in_i] ])
            in_i += 1
    
    # outgoing vertex handling

    for e in target_game[target_vertex].edges:
        G[mapping[outgoing_vertices[out_i]]].edges.add(e)
        out_i += 1

    G.dict.pop(target_vertex)
    G.redo_edges()
        
    return G


if __name__ == '__main__':
     # Wikipedia Graph
    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]

    wik_game = Game(zip(range(verts), info), edges)

    verts = 2
    info = [(0, 0), (0, 1)]
    edges = [(0, 1), (1, 0)]

    two_pair = Game(zip(range(verts), info), edges)

    ng = insert_game_into_vertices(two_pair, wik_game, set([0, 1]), seed=1008)

    ng.visualise(path='inserted.png')

    # wik_game.visualise(path='wikgame.png')
    # two_pair.visualise(path='twopair.png')