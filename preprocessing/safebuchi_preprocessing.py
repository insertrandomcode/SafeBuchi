import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.safe_buchi import safe_buchi_game
from algorithms.zielonkas import zielonkas
from base.attract import attract, safe_attract_star
from base.parity_game import Game
from preprocessing.preprocessor import Preprocessor

from typing import Tuple, Set

class SafeBuchiPreprocessor(Preprocessor):

    def preprocess(self, G: Game) -> Tuple[Game, Tuple[Set[int], Set[int]]]:
        partition = fatal_attractor_preprocessor(G, player=None)

        return G.exclude(partition[0]).exclude(partition[1]), partition

def fatal_attractor_preprocessor(G: Game, player: int) -> Set[int]:
    # Essentially runs the fatal attractor preprocessor - finding where a player can loop

    priorities = set([G[v].priority for v in G.nodes(lambda x : True if player is None else x.priority % 2 == player)])

    for p in priorities:
        player_ = p % 2
        loop_vertices = G.nodes(lambda x : x.priority == p)

        for _ in range(len(G)):
            prev = len(loop_vertices)

            loop_vertices = loop_vertices.intersection(safe_attract_star(G, player_, loop_vertices, lambda x : x.priority <= p))

            if prev == len(loop_vertices) or len(loop_vertices) == 0:
                break

        if len(loop_vertices) > 0:

            A = attract(G, player_, loop_vertices)

            W0, W1 = fatal_attractor_preprocessor(G.exclude(A), player)

            return ( W0.union(A), W1 ) if player_ == 0 else ( W0, W1.union(A) )
    
    return set([]), set([])

# deprecated version that uses subgame construction
def safe_buchi_preprocessing(G: Game) -> Tuple[Game, Tuple[Set[int], Set[int]]]:

    partition = [set([]), set([])]

    priorities = set([G[x].priority for x in G.nodes()])

    for _ in range(len(G)):

        new_vertices = 0

        for p in list(priorities):

            # find target_set and exclusion_set
            target_set = G.nodes(lambda x : x.priority == p)
            
            if len(target_set) == 0:
                continue

            exclusion_set = G.nodes(lambda x : x.priority > p)

            # create and solve safe buchi game
            safe_buchi_G = safe_buchi_game(target_set, exclusion_set, p % 2, G)
            winning_set = zielonkas(safe_buchi_G)[p % 2]

            # find attractor and exclude from game
            attr_winning_set = attract(G, p % 2, winning_set)
            partition[p % 2] = partition[p % 2].union(attr_winning_set)
            G = G.exclude(attr_winning_set)

            # count new vertices added
            new_vertices += len(attr_winning_set)
        
        # no new vertices added is an exit condition
        if new_vertices == 0:
            break
    
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


    


