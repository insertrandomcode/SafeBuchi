import sys
import json

def run_comparison(target1: str, target2: str, output: str):

    f1 = open(target1 + '/_filenames.txt', 'r')
    files1 = set(f1.readlines())
    f1.close()

    f2 = open(target2 + '/_filenames.txt', 'r')
    files2 = set(f2.readlines())

    filelist = files1.union(files2)

    analysis_json = {
        'left': target1,
        'right': target2
    }

    for key in ["both_solved", "left_only", "right_only", "neither_solved"]:
        analysis_json[key] = {
            "num_files": 0, 
            "time_left": 0, 
            "time_right": 0
        }
    
    analysis_json["l-error"] = []
    analysis_json["r-error"] = []

    targets = [target1, target2]

    for filename in filelist:
        analysis_json["both_solved"]
        
        fexists = [False, False]
        fjson = [None, None]
        freason = [None, None]

        for i in range(2):

            try:
                f = open(targets[i] + "/" + filename[:-1])
                fjson[i] = json.load(f)
                fexists[i] = True
                f.close()
            except FileNotFoundError:
                freason[i] = 'FileNotFound'

        # Handle case where one doesn't exist
        for i in range(2):
            if fexists[i] and fjson[i]["error"] is not None:
                fexists[i] = False
                freason[i] = fjson[i]["error"]

        if not all(fexists):
            for i, key in enumerate(['l-error','r-error']):
                if not fexists[i]:
                    analysis_json[key].append( (filename, freason[i]) )
            
            continue
                    
        # Ugly but it works
        if all([fjson[i]["solved"] for i in range(2)]):
            # both solved
            analysis = analysis_json["both_solved"]

        elif fjson[0]["solved"] and not fjson[1]["solved"]:
            # left only
            analysis = analysis_json["left_only"]

        elif (not fjson[0]["solved"]) and fjson[1]["solved"]:
            # right only
            analysis = analysis_json["right_only"]

        else:
            # neither
            analysis = analysis_json["neither_solved"]

        analysis["num_files"] += 1
        analysis["time_left"] += fjson[0]["preprocessing_time"]
        analysis["time_right"] += fjson[1]["preprocessing_time"]

    f = open(output, 'w')

    data = json.dumps(analysis_json, indent=4)
    f.write(data)

    f.close()

if __name__ == '__main__':
    _, target1, target2, output_file = sys.argv
    run_comparison(target1, target2, output_file)