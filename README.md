### Supplamental GitHub to a report for FIT3144

## Understanding the Code

`parity_game.py` implements the `Game` class that takes in a pair of lists as input: a list of vertices with their label and info (owner, priority) in tuple pairs and a list of all directed edges. It implements some useful methods such as exclude, invert_edges, nodes (a filter), and visuale. The visualise method utilises the pydot library that you may need to install.

`zielonkas.py` is a standard implementation of zielonkas recursive algorithm and the 'improved' attractor set calculation. `safe_buchi.py` creates a safe_buchi game from a game, target set and exclusion set. It uses the old model that includes all vertices but makes exclusion set have no outgoing edges but to 'lose', this is functionally identical to the updated version in the paper.

`safebuchi_preprocessing.py` is an implementation of the algorithm of the same name in the report, almost line for line. `multi_safebuchi.py` is an implementation of the version of the generalised safebuchi preprocessing with the 4 listed properties. We see here how we test the final property in polynomial time using a DP-like approach to remember.

Each '``driver`' function is what is used to run the final tests and the `analysis` functions read .res files created by the driver functions to aggregate data. If I'm being honest these 4 functions are very slap dash but they do what they need to. Note that the driver functions utilise linux to handle the timeouts and have not been tested on other operating systems.

## Understanding the Results

The zip file contains 6 folders. The analysis folder contains plaintext files containing the aggregate analysis data - understanding it is relatively straight-forward. Each results folder (including those within the randoms directories) contains a `_filenames.txt` which is used by the analysis functions and can be mostly ignored, a `_timing.txt` that contains timing info for each game, and the individual .res files for every game.

A .res file lists first the total number of vertices in the game, then number of vertices not solved. Then it lists the partition that was found and below that a printout of the remaining game in the same format as the .gm files.

## Running Benchmarks Yourself

If you wish to run the tests yourself download the benchmarks by going to https://github.com/jkeiren/paritygame-generator. Then download the random games contained in the zip file. Once you have all the .gm in appropriate directories construct a `_filenames.txt` file that contains a newline separated list of all names for each directory. Then call `driver.py testpath resultspath` where testpath is the path to the directory you wish to run the tests on (containing the `_filenames.txt`) and results path is where you want the results created. As the program runs it will generate .res files and add data to a `_timing.txt` file.

Note that if you want to run the same tests as me use only the tests listed in the `_filenames.txt` file the results have. Finally you may need to edit `read_into_game` in `driver.py`, as each benchmark uses slightly different formats there just comment out the irrelevant code and it will work.