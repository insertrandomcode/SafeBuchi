import sys
import json

def run_analysis(target: str, output: str):
    # get filenames
    
    f = open(target + '/_filenames.txt', 'r')
    filenames = f.readlines()
    f.close()

    # report on - total completely solved - avg solve %
    analysis_json = {
        "total_solved": 0,
        "total_unsolved": 0,
        "total_timeouts": 0,
        "total_files": 0,
        "solved_files_percentage": 0.0,
        "time_to_preprocess": 0,
        "time_to_pre_solve": 0,
        "time_to_zielonkas": 0,
        "incorrect_preprocessing": [],
        "unsolved": [],
        "solved": [],
        "timedout": []
    }

    for filename in filenames:

        f = open(target + "/" + filename[:-1])
        file_json = json.load(f)
        f.close()

        

        if file_json["error"] != None:
            if file_json["error"] == "Time Out Preprocessing in 10 minutes\n":
                analysis_json["total_files"] += 1
                analysis_json["timedout"].append(file_json["test_name"])
                analysis_json["total_timeouts"] += 1
            continue

        analysis_json["total_files"] += 1
        analysis_json["total_solved"] += file_json["solved"]
        analysis_json["total_unsolved"] += not file_json["solved"]
        analysis_json["time_to_preprocess"] += file_json["preprocessing_time"]
        analysis_json["time_to_pre_solve"] += file_json["pre_and_postprocessing_time"]
        analysis_json["time_to_zielonkas"] += file_json["zielonkas_time"]

        filelist = ""
        if file_json["solved"]:
            filelist = "solved"
        elif file_json["preprocess_correct"]:
            filelist = "unsolved"
        else:
            filelist = "incorrect_preprocessing"

        analysis_json[filelist].append(file_json["test_name"])
    
    analysis_json["solved_files_percentage"] = analysis_json["total_solved"] / analysis_json["total_files"]

    f = open(output, 'w')

    data = json.dumps(analysis_json, indent=4)
    f.write(data)

    f.close()

if __name__ == '__main__':
    # input directory name
    _, target_dir, output_file = sys.argv
    run_analysis(target_dir, output_file)

    # _, target1, target2, output_file = sys.argv
    # run_comparison(target1, target2, output_file)

    # run_tests('data', 'results')