import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Set, Tuple, List
import signal # this file relies on Unix
import time
from contextlib import contextmanager
from abc import ABC, abstractmethod
import json

from base.parity_game import Game

# Code Heavily Based off of answer by Josh Lee
#   from - https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call
# Handles timouts using signal processing

class TimeoutException(Exception): pass

#TODO: understand the code
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed Out")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

class Driver(ABC):

    def __init__(self):
        self.results = {} # JSON of each resulting item

    @abstractmethod
    def test(self, input_file: str) -> None:
        pass

    def read_into_game(self, input_file: str) -> Game:
        f = open(input_file, 'r')

        _ = f.readline() # opening line
        _ = f.readline() # start location -- mlsolver only

        info, edges = [], []

        while True:
            # read in data - ignoring the name and semicolon
            data = f.readline().split(' ')

            # could be more robust
            if data == [''] or data[0] == 'timeout:' or data == []:
                break

            label = int(data[0])
            priority = int(data[1])
            owner = int(data[2])
            # destinations = [] if len(data) == 3 else list(map(int, ''.join(data[3:])[:-2].split(','))) # spaces
            destinations = [] if len(data) == 3 else list(map(int, data[3][:-2].split(','))) # no spaces

            info.append( (label, (owner, priority)))
            for dest in destinations:
                edges.append((label, dest))
    
        f.close()

        return Game(info, edges)

    def write_results(self, target_dir: str) -> None:

        for key in self.results:
            result = self.results[key]

            f = open(target_dir + "/" + result["test_name"][:-3] + ".json", 'w')

            result_json = json.dumps(result)
            f.write(result_json)

            f.close()

        self.results.clear()
    
    def filelist(self, target_dir: str) -> List[str]:
        
        ## generates a list of files to run from the _filelist.txt file in a directory

        f = open(target_dir + "/_filenames.txt" ,'r')

        filenames = f.read().split('\n')

        filenames = list(map(lambda s : target_dir + "/" + s, filter(lambda s: len(s) > 0, filenames)))

        f.close()
        
        return filenames



