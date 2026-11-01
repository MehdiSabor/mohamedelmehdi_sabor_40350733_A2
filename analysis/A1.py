# You can import the necessary libraries
import ast
import os
import subprocess
import sys
from dotenv import load_dotenv


def A1(PATH_TO_Q2_T3)->dict[int,float]:
    """
    Returns the dictionary of (number of workers,TimeTaken)
    hint: observe how MPI is being called in test.py
    """
    average_times = {}

    for workers in range(1, 11):
        total_time = 0.0

        for run in range(3):
            command = [
                'mpirun', '-n', str(workers), sys.executable,
                PATH_TO_Q2_T3,
            ]
            try:
                output = subprocess.run(
                    command, text=True, capture_output=True, check=True,
                )
            except subprocess.CalledProcessError as error:
                raise RuntimeError(
                    f"Q2 T3 failed with {workers} workers on run {run + 1}: "
                    f"{error.stderr.strip()}"
                ) from error

            result = ast.literal_eval(output.stdout)

            if isinstance(result['final_answer'], str):
                raise RuntimeError(result['final_answer'])

            total_time = total_time + result['totalTimeTaken']
            print(f"Workers {workers}, run {run + 1} finished: {result['totalTimeTaken']} seconds", flush=True)

        average_times[workers] = total_time / 3
        print(f"Workers {workers} finished: average {average_times[workers]} seconds", flush=True)

    return average_times

if __name__ == "__main__":
    load_dotenv()
    print(A1(os.getenv('PATH_q2_t3')))
