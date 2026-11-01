import sys
import ast
import subprocess
from dotenv import load_dotenv
import os
sys.path.append(os.getcwd()) 
sys.path.append(os.path.abspath('../')) 
load_dotenv()
DATA_PATH = os.getenv('PATH_DATASET')
from implementation.q3.t1 import ThreadingSolution
from implementation.q3.t2 import MultiProcessingSolution

# Import the necessary libraries and implementations
def A2(PATH_TO_Q3_T3)->dict[str,dict[int,float]]:
    """
    Return a dictionary of format {MT:{1:t1,2:t2, ..}, MP:{...}, MPI:{...}} where t is the time in seconds.
    hint: observe how objects and libraries are being called in test.py
    """
    average_times = {"MT": {}, "MP": {}, "MPI": {}}

    for technique in ["MT", "MP", "MPI"]:
        for workers in range(1, 11):
            total_time = 0.0

            for run in range(3):
                if technique == "MT":
                    solution = ThreadingSolution(
                        num_of_threads=workers,
                        dataset_path=DATA_PATH,
                        dataset_size=3000000,
                    )
                    final_answer, chunk_sizes, answers, elapsed = solution.run()

                elif technique == "MP":
                    solution = MultiProcessingSolution(
                        num_of_processes=workers,
                        dataset_path=DATA_PATH,
                        dataset_size=3000000,
                    )
                    final_answer, chunk_sizes, answers, elapsed = solution.run()

                else:
                    command = [
                        'mpirun', '-n', str(workers), sys.executable,
                        PATH_TO_Q3_T3,
                    ]
                    try:
                        output = subprocess.run(
                            command, text=True, capture_output=True, check=True,
                        )
                    except subprocess.CalledProcessError as error:
                        raise RuntimeError(
                            f"Q3 T3 failed with {workers} workers on run {run + 1}: "
                            f"{error.stderr.strip()}"
                        ) from error

                    result = ast.literal_eval(output.stdout)
                    final_answer = result['final_answer']
                    elapsed = result['totalTimeTaken']

                if isinstance(final_answer, str):
                    raise RuntimeError(final_answer)

                total_time = total_time + elapsed
                print(f"{technique}: workers {workers}, run {run + 1} finished: {elapsed} seconds", flush=True)

            average_times[technique][workers] = total_time / 3
            print(f"{technique}: workers {workers} finished: average {average_times[technique][workers]} seconds", flush=True)

    return average_times

if __name__ == "__main__":
    print(A2(os.getenv('PATH_q3_t3')))
