from safe_buchi import safe_buchi_game
from zielonkas import zielonkas, attract
from parity_game import Game

from typing import Tuple, Set

def safe_buchi_preprocessing(G: Game) -> Tuple[Game, Tuple[Set[int], Set[int]]]:

    partition = [set({}), set({})]

    priorities = set([G[x].priority for x in G.nodes()])

    for p in list(priorities):

        # find target_set and exclusion_set
        target_set = G.nodes(lambda x : x.priority == p)
        
        if target_set == set([]):
            continue

        exclusion_set = G.nodes(lambda x : x.priority > p)

        # create and solve safe buchi game
        safe_buchi_G = safe_buchi_game(target_set, exclusion_set, p % 2, G)
        winning_set = zielonkas(safe_buchi_G)[p % 2]

        # find attractor and exclude from game
        attr_winning_set = attract(G, p % 2, winning_set)
        partition[p % 2] = partition[p % 2].union(attr_winning_set)
        G = G.exclude(attr_winning_set)
    
    return G, partition

if __name__ == '__main__':
    # Wikipedia Graph
    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]
    wik_game = Game(zip(range(verts), info), edges)

    post_game, partition = safe_buchi_preprocessing(wik_game)

    print(partition)


    


