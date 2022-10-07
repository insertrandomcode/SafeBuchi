from multi_safebuchi import multi_safe_preprocessing
from zielonkas import zielonkas
from driver import time_limit, read_into_game, TimeoutException
import time

def run_tests(test_dir: str, result_dir: str) -> None:
    f = open(test_dir + "/_filenames.txt" ,'r')

    filenames = f.read().split('\n')

    f.close()

    for filename in filenames:
        print(f'------- {filename} ------')

        try:
            with time_limit(5 * 60): # 5 min lim
                G = read_into_game(test_dir + '/' + filename)
        except TimeoutException as e:
            print("Timed Out")
            continue

        print(f'Game Loaded')

        try:
            with time_limit(10 * 60):
                start_multi = time.time()
                partition1 = multi_safe_preprocessing(G)
                end_multi = time.time()
        except TimeoutException as e:
            print("Timed Out")
            continue

        print('Ran Solution With Multi Safe Buchi')
        
        try:
            with time_limit(10 * 60):
                start_zlk = time.time()
                partition2 = zielonkas(G)
                end_zlk = time.time()
        except TimeoutException as e:
            print("Timed Out")
            continue

        print('Ran Solution With Zielonkas')

        write_data(result_dir + '/' + filename[:-3] + '.res', partition1 == partition2, 
                             end_multi - start_multi,
                             end_zlk - start_zlk)

def write_data(filepath: str, correctness: bool, mult_time: float, zlk_time: float):
    f = open(filepath, 'w')

    f.write(f'Multi Corr: {correctness}\n')
    f.write(f'T[ MB]: {mult_time}\n')
    f.write(f'T[ZLK]: {zlk_time}\n')

    f.close()

import sys
if __name__ == '__main__':
    # input directory name
    _, test_dir, result_dir = sys.argv
    run_tests(test_dir, result_dir)

    # run_tests('data', 'results')