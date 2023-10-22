## Supplamental GitHub to thesis for FIT4444

### Understanding the Code

#### Basics of Parity Games
`parity_game.py` implements the `Game` class that takes in a pair of lists as input: a list of vertices with their label and info (owner, priority) in tuple pairs and a list of all directed edges. It implements some useful methods such as exclude, invert_edges, nodes (a filter), and visuale. The visualise method utilises the pydot library that you may need to install.

`attract.py` implementes the various forms of the attractor calculation, including star and safe variants. 

`zielonkas.py` is a standard implementation of zielonkas recursive algorithm and the improved attractor set calculation.

#### Preprocessing

`fatalattractor_preprocessing.py` contains the `FatalAttractorPreprocessor` that contains implements the fatal attractor calculations developed by Huth et al. as `fatal_attractor_underestimator`. It also contan the `safe_buchi_underestimator` that makes the same calculation with a slower method.

`WinningCorePreprocessor` implemented in `winnincores/winning_core_underestimation.py` is an implementation of the winning core under-approximator from Vester. 

In the `tangletraps` directory the file `tangletraps/tangle_traps.py` implements the pre-target tangle avoidance algorithm. This includes an implementation of tangle labelling, and the tangle underestimation techniques used.

#### Testing

The `testing` directory contains the testing harness. The file `testing/preprocessing_driver.py` contains the preprocessor the testing will run on and runs the tests, `testing/testing_driver.py` contains the functions to read the files into a `Game` object. The `testing/data_analysis.py` and `testing/data_comparison.py` collate the results into a single json, for a single directory or pair of directories respectively.

#### Other Code

The repo contains various other algorithms that were developed over the year before arriving at ptta, I have left these for posterity but each is either theoretically incorrect or underpowered and thus can be ignored. Additionally, many will have not been updated in some time and likely will simply not run.

### Understanding the Results

The results in `results_collation.zip` give for each set of games, and for each preprocessor tested, the filelists for games solved/unsolved/timedout and the times it took to solve the games that didn't time out.

### Running Benchmarks Yourself

If you wish to run the tests yourself download the benchmarks by going to https://github.com/jkeiren/paritygame-generator. Once you have all the .gm in appropriate directories construct a `_filenames.txt` file that contains a newline separated list of all names for each directory `ls > _filenames.txt`. Then call `python testing/preprocessing_driver.py testpath resultspath` where testpath is the path to the directory you wish to run the tests on (containing the `_filenames.txt`) and results path is where you want the results created. Note that `preprocessing_driver.py` uses UNIX signals for timing and so will not run on Windows. As the program runs it will generate .json files each containing detailed results of an individual test. To collate these, add a `_filenames.txt` file to the results directory and make a `python testing/data_analysis.py resultspath analysisfilepath` and it will output a .json file with the collated results.

Finally you may need to edit `read_into_game` in `testing_driver.py`, as each benchmark uses slightly different formats, doing so is a matter of commenting out the lines indicated for each pair.