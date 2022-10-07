import numpy as np
from typing import Set, Tuple, List
from parity_game import Game
from safe_buchi import safe_buchi_game
from zielonkas import zielonkas, attract

# Could avoid using dicts but I'll handle that later
def multi_safe_preprocessing(G: Game, debug: bool = False) -> Tuple[Tuple[Set[int], Set[int]]]:
    # Just doing it for Even as it should be enough
    # Get set of even priorities and init edge_checking dict
    even_p = set([])
    _can_win = {}

    for node in G.nodes():
        if G[node].priority % 2 == 0:
            even_p.add(G[node].priority)
    
    even_p = sorted(list(even_p), reverse=True)

    # Step 1: do the single SafeBuchi game on the largest even priority
    target_set = G.nodes(lambda x : x.priority == even_p[0])
    exclusion_set = G.nodes(lambda x : x.priority > even_p[0])
    safe_buchi_G = safe_buchi_game(target_set, exclusion_set, 0, G)
    winning_set = zielonkas(safe_buchi_G)[0]
    attr_winning_set = attract(G, 0, winning_set)
    tmp = {}
    for node in G.nodes():
        tmp[node] = False
    for node in attr_winning_set:
        tmp[node] = True
    _can_win[0] = tmp

    # for increasing ranges, solve the game passing the winning_dict as a test for the edges
    for i in range(1, len(even_p)):
        tmp = {}
        SB = create_multi_sb(G, i, even_p, _can_win)
        winning_set = zielonkas(SB)[0]
        attr_winning_set = attract(G, 0, winning_set)
        for node in G.nodes():
            tmp[node] = False
        for node in attr_winning_set:
            tmp[node] = True
        _can_win[i] = tmp
    
    if debug:
        return (attr_winning_set, G.nodes().difference(attr_winning_set)), _can_win

    return (attr_winning_set, G.nodes().difference(attr_winning_set))

def create_multi_sb(G: Game, i: int, even_p: List[int], _can_win) -> Game:
    info = [('sink', (0, 1))]
    edges = [('sink', 'sink')]

    vertices = G.nodes(lambda x : x.priority <= even_p[0])

    for vertex in vertices:
        _info = (vertex, (G[vertex].owner, 2 if G[vertex].priority in even_p[:i+1] else 1))

        to_sink = False
        for dest in G[vertex].edges:
            if G[dest].priority > even_p[0]:
                to_sink = True
            elif G[dest].priority <= G[vertex].priority or G[dest].priority <= even_p[i] or G[dest].priority in even_p[:i+1]:
                edges.append((vertex, dest))
            else:
                # Check the can_win
                for j in range(i-1, -1, -1):
                    if even_p[j] > G[dest].priority:
                        break
                assert 0 <= j < i, f'j: {j} not in correct range'
                if any([_can_win[k][dest] for k in range(0,j+1)]):
                    edges.append((vertex, dest))
                else:
                    to_sink = True
        
        if to_sink:
            edges.append((vertex, 'sink'))
        info.append(_info)
    
    return Game(info, edges)

from driver import read_into_game
from safebuchi_preprocessing import safe_buchi_preprocessing
# FML - this is wrong.

if __name__ == '__main__':
    # # Wikipedia Graph
    # verts = 8
    # info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    # edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
    #          (5,7), (6,1), (6,7), (7,2), (7, 5)]

    # wik_game = Game(zip(range(verts), info), edges)

    # partition = multi_safe_preprocessing(wik_game)
    
    # print(partition)

    G = read_into_game('modelchecking/data/ABP(BW)datasize=2_infinitely_often_read_write.gm')
    # G.visualise()
    partition1, can_win = multi_safe_preprocessing(G, True)
    partition2 = zielonkas(G)
    post_G, partition3 = safe_buchi_preprocessing(G)
    # Hmm, MSP sees all win odd, ZLK sees all win even

    print(partition1 == partition2)
    # print(can_win[1])
    print(partition1)
    print(partition2)