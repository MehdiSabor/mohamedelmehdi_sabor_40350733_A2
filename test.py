"""
This is sample testing script, It is only for testing your code is working or not.
** It doesn't guarantee that your solution is 100% correct **
It tests that you have followed guidelines given in handout - * No global functions or variables *
"""
from implementation.q1.t1 import ThreadingSolution as Q1T1
from implementation.q1.t2 import MultiProcessingSolution as Q1T2

from implementation.q2.t1 import ThreadingSolution as Q2T1
from implementation.q2.t2 import MultiProcessingSolution as Q2T2

from implementation.q3.t1 import ThreadingSolution as Q3T1
from implementation.q3.t2 import MultiProcessingSolution as Q3T2

from implementation.q4.t1 import ThreadingSolution as Q4T1
from implementation.q4.t2 import MultiProcessingSolution as Q4T2

from analysis.A1 import A1 as A1
from analysis.A2 import A2 as A2
import ast
from dotenv import load_dotenv
import os
load_dotenv()

def print_answer(obj,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken):
    class_name=obj.__class__.__name__ if not isinstance(obj,str) else "MPI"
    obj_name = [var_name for var_name, var_obj in globals().items() if var_obj is obj][0] if not isinstance(obj,str) else obj
    print(f"Question:{obj_name}\t instance of class {class_name}")
    print(f"{obj_name}->Final Answer:{final_answer}")
    print(f"{obj_name}->ChunkSizes: Min={min(chunkSizePerThread)}\tMAX={max(chunkSizePerThread)}\tAverage={sum(chunkSizePerThread)/len(chunkSizePerThread)}")
    print(f"{obj_name}->Intermediate Answers: {[str(elem) for elem in answerPerThread]} ")
    print(f"{obj_name}->TotalTimeTaken: {totalTimeTaken}")
    print(f"########################################################")

def run_mpi(num_workrs,task_path):
    import subprocess
    # Define the command to run the MPI program
    command = ['mpirun', '-n', str(num_workrs), 'python', task_path]
    try:
        out = subprocess.run(command, text=True, capture_output=True, check=True)    
        return tuple(ast.literal_eval(out.stdout).values())
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the MPI program.")
        print("Return code:", e.returncode)
        print("Output:\n", e.stdout)
        print("Errors:\n", e.stderr)


if __name__ == '__main__':
    DATA_PATH = os.getenv('PATH_DATASET')
    PATH_Q2_t3 = os.getenv('PATH_q2_t3')
    PATH_Q3_t3 = os.getenv('PATH_q3_t3')
    # Test Question 1
    q1t1 = Q1T1(num_of_threads=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q1t1.run()
    print_answer(q1t1,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    q1t2 = Q1T2(num_of_processes=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q1t2.run()
    print_answer(q1t2,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    #################### Run MPI Program As a cluster of workers using subprocess command #################
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken=run_mpi(4,"implementation/q1/t3.py")
    print_answer('q1t3',final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)


    # Test Question 2
    q2t1 = Q2T1(num_of_threads=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q2t1.run()
    print_answer(q2t1,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    q2t2 = Q2T2(num_of_processes=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q2t2.run()
    print_answer(q2t2,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    #################### Run MPI Program As a cluster of workers using subprocess command #################
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken=run_mpi(4,"implementation/q2/t3.py")
    print_answer('q2t3',final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)


    # Test Question 3
    q3t1 = Q3T1(num_of_threads=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q3t1.run()
    print_answer(q3t1,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    q3t2 = Q3T2(num_of_processes=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q3t2.run()
    print_answer(q3t2,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    #################### Run MPI Program As a cluster of workers using subprocess command #################
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken=run_mpi(4,"implementation/q3/t3.py")
    print_answer('q3t3',final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)


    # Test Question 4
    q4t1 = Q4T1(num_of_threads=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q4t1.run()
    print_answer(q4t1,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    q4t2 = Q4T2(num_of_processes=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken= q4t2.run()
    print_answer(q4t2,final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)
    #################### Run MPI Program As a cluster of workers using subprocess command #################
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken=run_mpi(4,"implementation/q4/t3.py")
    print_answer('q4t3',final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken)

    # Test analysis A1
    dict_A1=A1(PATH_Q2_t3)
    print("")
    if len(dict_A1)==10:
        print(f"A1 analysis:{dict_A1}")
    # Test analysis A2
    dict_A2=A2(PATH_Q3_t3)
    if len(dict_A2)==3:
        print(f"A2 analysis:")
        for key in dict_A2.keys():
            print(f"{key}:{dict_A2[key]}")