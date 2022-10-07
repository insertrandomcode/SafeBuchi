import sys

def run_analysis(target: str, output: str):
    # get filenames
    
    f = open(target + '/_timing.txt', 'r')
    lines = f.readlines()
    f.close()

    avg_rel, total_files = 0, 0
    avg_sb_total, avg_zl = 0, 0

    i = 0
    while i + 5 <= len(lines):
        cur_lines = lines[i:i+5]

        total_files += 1

        sb_data = cur_lines[1][11:].split()
        zl_data = cur_lines[2][11:].split()

        sb_total = float(sb_data[0])
        sb_sb_time = float(sb_data[2])
        sb_zl_time = float(sb_data[4])
        zl_total = float(zl_data[0])

        avg_rel += sb_total / zl_total
        avg_sb_total += sb_total
        avg_zl += zl_total

        i += 5

    analysis = [f'Analysis of Files in directory {target_dir}:\n\n',
                f'Avg Time Ratio -- {avg_rel / total_files}\n',
                f'Avg SB total -- {avg_sb_total / total_files}\n',
                f'Avg ZRA total -- {avg_zl / total_files}\n']

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
