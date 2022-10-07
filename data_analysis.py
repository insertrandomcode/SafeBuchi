import sys

def run_analysis(target: str, output: str):
    # get filenames
    
    f = open(target + '/_filenames.txt', 'r')
    filenames = f.readlines()
    f.close()

    # report on - total completely solved - avg solve %
    solved_files, avg_solve, total_files, total_solve, total_nodes = 0, 0, 0, 0, 0
    total_nodes_from_unsolved = 0

    for filename in filenames:

        f = open(target + '/' + filename[:-1])

        f_size, f_nodes_left = map(int, f.readline().strip('\n').split(' '))

        solved_files += (f_nodes_left == 0)
        avg_solve += 1 - f_nodes_left/f_size
        total_solve += f_size - f_nodes_left
        total_files += 1
        total_nodes += f_size
        if f_nodes_left != 0:
            total_nodes_from_unsolved += 1 - f_nodes_left/f_size

        f.close()

    analysis = [f'Analysis of Files in directory {target_dir}:\n\n'
                f'{solved_files/total_files} -- Files Solved % -- {solved_files}, {total_files}\n', 
                f'{avg_solve / total_files} -- Avg Solve per File --\n',
                f'{total_solve/total_nodes} -- Nodes Solved % -- {total_solve}, {total_nodes}\n',
                f'{total_nodes_from_unsolved / (total_files - solved_files)} -- Avg Solve per Unsolved File -- \n'
                f'follows is the list of files analysed:\n\n'] + filenames
    try:
        f = open(output, 'w')
    except FileNotFoundError:
        f = open(output, 'x')

    f.writelines(analysis)

    f.close()




if __name__ == '__main__':
    # input directory name
    _, target_dir, output_file = sys.argv
    run_analysis(target_dir, output_file)

    # run_tests('data', 'results')
