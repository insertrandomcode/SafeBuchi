import sys
from typing import Set, Tuple
# timeouts
import signal
import time
from contextlib import contextmanager

from parity_game import Game
from safebuchi_preprocessing import safe_buchi_preprocessing
from zielonkas import zielonkas

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


def run_tests(test_dir: str, result_dir: str) -> None:
    # get filelist of .gm files from a filelist.txt file
    f = open(test_dir + "/_filenames.txt" ,'r')

    filenames = f.read().split('\n')

    f.close()

    # for file in filelise
    for filename in filenames:

        print(f'------- {filename} ------')
        finished_preprocessing, finished_run = True, True

        # read in game into Game format
        try:
            with time_limit(5 * 60): # 5 min lim
                G = read_into_game(test_dir + '/' + filename)
        except TimeoutException as e:
            print("Timed Out")
            continue

        print(f'Game Loaded')

        # run preprocessing

        try:
            start_with_preprocessing = time.time()
            with time_limit(20 * 60): # 20 min time limit
                post_G, partition = safe_buchi_preprocessing(G)
                start_zie_with_preprocessing = time.time()
                partition1 = zielonkas(post_G)
                partition1 = (partition[0].union(partition1[0]), partition[1].union(partition1[1]))
            end_with_preprocessing = time.time()

        except TimeoutException as e:
            # if times out just pass
            print("Timed Out")
            finished_preprocessing = False
        print('Ran Solution With Preprocessing Complete')

        try:
            start_no_preprocessing = time.time()
            with time_limit(20 * 60): # 20 min time limit
                partition2 = zielonkas(G)
            end_no_preprocessing = time.time()

        except TimeoutException as e:
            # if times out just pass
            print("Timed Out")
            finished_run = False
        print('Ran Solution Without Preprocessing Complete')

        if (finished_preprocessing):
        # create and write to results directory
            write_data(result_dir + '/' + filename[:-3] + '.res', G, post_G, partition)
        
            if (finished_run):
                write_timing(result_dir + '/_timing.txt', end_with_preprocessing - start_with_preprocessing
                                                        , start_zie_with_preprocessing - start_with_preprocessing
                                                        , end_no_preprocessing - start_no_preprocessing
                                                        , filename
                                                        , partition1
                                                        , partition2)


def write_timing(filepath: str, preprocess_total_time: float, preproess_process_time: float, 
                 no_preprocess_time: float, filename: str, partition1, partition2) -> None:
    f = open(filepath, 'a')

    f.write(f'----- {filename} -----\n')
    f.write(f'Time[ SB]: {preprocess_total_time} = {preproess_process_time} + {preprocess_total_time - preproess_process_time}\n')
    f.write(f'Time[NSB]: {no_preprocess_time}\n')

    f.write(f'Equiv: {partition1 == partition2}\n\n')

    f.close()
    

def read_into_game(filepath: str) -> Game:
    f = open(filepath, 'r')

    _ = f.readline() # opening line
    _ = f.readline() # start location

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
        # destinations = [] if len(data) == 3 else list(map(int, ''.join(data[3:])[:-2].split(',')))
        destinations = [] if len(data) == 4 else list(map(int, data[3].split(',')))

        info.append( (label, (owner, priority)))
        for dest in destinations:
            edges.append((label, dest))
    
    f.close()

    return Game(info, edges)

def write_data(filepath: str, G: Game, post_G: Game, partition: Tuple[Set[int], Set[int]]) -> None:
    f = open(filepath, 'w')

    f.write(f'{len(G.dict)} {len(post_G.dict)}\n')
    f.write(f'{partition}\n')
    f.write(f'----------------------- post_Game ------------------------\n')

    for vertex in post_G.nodes():
        f.write(f'{vertex} {post_G[vertex].priority} {post_G[vertex].owner} {",".join(map(str, post_G[vertex].edges))};\n')

    f.close()



if __name__ == '__main__':
    # input directory name
    _, test_dir, result_dir = sys.argv
    run_tests(test_dir, result_dir)

    # run_tests('data', 'results')
