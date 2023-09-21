from testing.preprocessing_driver import PreprocessingDriver
from base.parity_game import Game
from base.attract import attract, safe_attract_star
from base.labelling import labelling, Label, labelling_nostop
from algorithms.zielonkas import zielonkas
from preprocessing.winningcores.winning_core_underestimation import winning_core_underapproximation, WinningCorePreprocessor
from preprocessing.three_preprocessors import SequentialPreprocessor, TwoPreprocessors, ThreePreprocessors
from preprocessing.safebuchi_preprocessing import safe_buchi_preprocessing, SafeBuchiPreprocessor
from preprocessing.trapfinding.trap_finding_class import trap_finding_underapproximation, TrapFindingPreprocessor
from preprocessing.strategyfinding.strategy_preprocessor import StrategyFindingPreprocessor, strategy_underestimation, losing_edges
from preprocessing.strategyfinding.strategy_finding import strategy_graph, auxiliary_graph, WGraph
from preprocessing.layeredmazes.vertex_cover_layering import vertex_cover_layering
from preprocessing.infinitelabels.infinite_preprocessor import InfiniteMaxLabelPreprocessor, infinite_label_underestimation, find_infinite_label
from preprocessing.infinitelabels.staggered_traps import StaggeredTrapPreprocessor, staggered_trap_underestimation
from preprocessing.infinitelabels.tangle_traps import TangleTrapPreprocessor, tangle_trap_underestimation, tangle_labelling, get_tangle_accessories
from base.tarjan_scc import tarjan_scc
from base.game_insert import insert_game_into_vertices

import pydot
from typing import Set

#TODO: look into specific steps to confirm

def get_x(G: Game, player: int) -> Set[int]:
        player = 0
        X = G.nodes(lambda x : x.owner == 1-player)

        for _ in range(len(G.nodes())):

            labels = labelling(G, X, player)

            next_ = set([x for x in X if labels[x].value >= 0])

            if X == next_:
                break
        
            X = next_
        
        return X

if __name__ == '__main__':

    #################################### Games ####################################

    # G = PreprocessingDriver("empty").read_into_game('games/modelchecking/Elevatorpolicy=LIFO_storeys=2_always_if_max_floor_requested_eventually_at_max_floor.gm')
    # G = PreprocessingDriver("empty").read_into_game('games/modelchecking/SWPdatasize=2_windowsize=1_infinitely_often_read_write.gm')
    # G = PreprocessingDriver("empty").read_into_game('games/modelchecking/ABPdatasize=2_infinitely_often_read_write.gm')
    # G = PreprocessingDriver("empty").read_into_game('games/modelchecking/Hanoindisks=8_eventually_done.gm')
    # G = PreprocessingDriver("empty").read_into_game('games/modelchecking/Pardatasize=2_infinitely_often_enabled_then_infinitely_often_taken.gm')
    # G = PreprocessingDriver("empty").read_into_game('games/modelchecking/Hesselinkdatasize=2_nodeadlock.gm')
    # G = PreprocessingDriver("empty").read_into_game('games/equivchecking/ABP_SWP_(datasize=2_capacity=1_windowsize=1)eq=branching-bisim.gm')
    # print("loaded")

    # Game for which the is_maze strategy graph algorithm fails on [0, 6] -- notably still solved properly - likely by chance.
    # vertices = range(8)
    # info = [(1, 1), (0, 3), (1,3), (0,5), (0, 8), (0, 7), (1, 1), (0, 4)]
    # edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 1), (3, 0), (0, 5), (5, 6), (6, 4), (4,0), (6,7), (7, 6)]

    # G = Game(zip(vertices, info), edges)

    ################################## Attempting to Beat Tangle #################################

    M = Game(
        zip( range(4),
        [(1,0), (0,1), (1,0), (0,2)]),
        [(0,0), (0,1), (1,2), (2,2), (2,3), (3,0)]
    )

    Mz = Game(
        zip(range(7),
        [(1,1), (0,7), (0,11), (1,1), (0,12), (0,7), (0,0)]), # change 12 to 13 to test for overcorrection
        [(0,1), (1,2), (1,5), (2,3), (3,4), (4,5), (5,0), (0,6), (3,6), (6,6)]
    )

    Mzs = insert_game_into_vertices(Mz, M, set([0, 3]), lambda x : x.owner == 1, seed=42)
    tangles = [[11, 12, 13, 14], [8, 9, 10, 7]]
    in_tangle, tangle_edges = get_tangle_accessories(Mzs, tangles, 0)
    X = [5, 6, 10, 12, 13]

    l = tangle_labelling(Mzs, X, 0, tangles, in_tangle, tangle_edges)

    # print(l)

    G = Mzs

    # print(list(map(len, zielonkas(G))))
    # print(list(map(len, tangle_trap_underestimation(G, debug=True))))