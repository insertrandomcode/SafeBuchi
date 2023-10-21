import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import List

from base.parity_game import Game
from preprocessing.preprocessor import Preprocessor

class SequentialPreprocessor(Preprocessor):

    def __init__(self, preprocessor_list: List[Preprocessor]):
        # These should be initialised
        self.preprocessor_list = preprocessor_list
    
    def preprocess(self, G: Game):
        
        partition = [set([]), set([])]

        maxiter = len(G)
        for _ in range(maxiter):
            
            N = len(G)

            p_list = []

            num_solved = 0

            for P in self.preprocessor_list:
                G, p = P.preprocess(G)

                partition[0] = partition[0].union(p[0])
                partition[1] = partition[1].union(p[1])

                num_solved += len(p[0]) + len(p[1])

                if len(G) == 0:
                    break

            if len(G) == N or num_solved == 0:
                break
        
        return G, partition
