import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Set, Tuple, List
import time

from base.parity_game import Game
from algorithms.zielonkas import zielonkas
from preprocessing.preprocessor import Preprocessor
from testing.testing_driver import Driver, time_limit, TimeoutException

class PreprocessingDriver(Driver):

    def __init__(self, preprocessor: Preprocessor) -> None:
        self.preprocessor = preprocessor
        
        super().__init__()
    
    def test(self, input_file: str) -> str:

        # JSON (dict) of test
        self.results[input_file] = {"error": None, "preprocess_correct": False, "solved": False}

        try:
            self.results[input_file]["test_name"] = input_file[len(input_file) - input_file[::-1].index('/'):]
        except ValueError:
            self.results[input_file]["test_name"] = input_file

        # read file into game
        try:
            with time_limit(5 * 60): # 5 min lim
                G = self.read_into_game(input_file)
        except TimeoutException as e:
            self.results[input_file]["error"] = f"Timed Out Reading File in 5 minutes\n"
            return "Timed Out when reading"

        # self.results[input_file]["game"] = G

        # Preprocessing Test
        try:
            with time_limit(10 * 60):
                start_preprocessing = time.time()
                post_G, partition = self.preprocessor.preprocess(G)
                end_preprocessing = time.time()
        except TimeoutException as e:
            self.results[input_file]["error"] = f"Time Out Preprocessing in 10 minutes\n"
            return "Timed Out Preprocessing"

        self.results[input_file]["preprocessing_time"] = end_preprocessing - start_preprocessing
        self.results[input_file]["preprocessing_partition"] = list(map(list,partition))
        # self.results[input_file]["postprocessing_game"] = post_G

        try:
            with time_limit(10 * 60):
                start_postprocessing = time.time()
                post_partition = zielonkas(post_G)
                end_postprocessing = time.time()
        except TimeoutException as e:
            self.results[input_file]["error"] = f"Time Out Postprocessing in 10 minutes\n"
            return "Timed Out Postprocessing"

        self.results[input_file]["postprocessing_time"] = end_postprocessing - start_postprocessing
        self.results[input_file]["postprocessing_partition"] = list(map(list,post_partition))
        self.results[input_file]["pre_and_postprocessing_time"] = self.results[input_file]["postprocessing_time"] + self.results[input_file]["preprocessing_time"]
        
        try:
            with time_limit(10 * 60):
                start_zielonkas = time.time()
                final_partition = zielonkas(G)
                end_zielonkas = time.time()
        except TimeoutException as e:
            self.results[input_file]["error"] = f"Time Out Running Zielonkas in 10 minutes\n"
            return "Timed Out Zielonkas"

        self.results[input_file]["zielonkas_time"] = end_zielonkas - start_zielonkas
        self.results[input_file]["zielonkas_partition"] = list(map(list,final_partition))
        self.results[input_file]["preprocess_correct"] = final_partition[0].issuperset(partition[0]) and final_partition[1].issuperset(partition[1])
        self.results[input_file]["solved"] = partition[0] == final_partition[0] and partition[1] == final_partition[1]

        return "Completed Test"

if __name__ == '__main__':
    _, test_dir, result_dir = sys.argv

    from preprocessing.winningcores.winning_core_underestimation import WinningCorePreprocessor
    from preprocessing.infinitelabels.tangle_traps import TangleTrapPreprocessor
    from preprocessing.three_preprocessors import SequentialPreprocessor
    from preprocessing.safebuchi_preprocessing import SafeBuchiPreprocessor

    ## Change Preprocessor Here
    T = PreprocessingDriver(SafeBuchiPreprocessor())
    #  = PreprocessingDriver(SequentialPreprocessor([SafeBuchiPreprocessor(), WinningCorePreprocessor()]))
    
    filelist = T.filelist(test_dir)

    for filename in filelist:
        print(f"########## {filename} #########")
        print( T.test(filename) )
        T.write_results(result_dir)

    # T.write_results(result_dir)
