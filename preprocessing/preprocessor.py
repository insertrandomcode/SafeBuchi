import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.parity_game import Game

from typing import Set, Tuple
from abc import ABC, abstractmethod



class Preprocessor(ABC):

    # don't know whether or not to keep logs but we'll make it general for now

    @abstractmethod
    def preprocess(self, G: Game) -> Tuple[Game, Tuple[Set[int], Set[int]]]:
        pass