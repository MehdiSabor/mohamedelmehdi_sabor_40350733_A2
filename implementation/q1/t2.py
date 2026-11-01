"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.
"""
import time
from dotenv import load_dotenv
import os
load_dotenv()
import pandas as pd
from multiprocessing import Pool


class MultiProcessingSolution:
    """
    You are allowed to implement as many helper methods and variables as you wish
    """
    def __init__(self, num_of_processes=None, dataset_path=None, dataset_size=None):
        self.num_of_processes = num_of_processes
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size

    def count_chunk(self, chunk):
        start, end = chunk
        if start == end:
            return 0

        df = pd.read_csv(
            self.dataset_path, skiprows=1 + start, nrows=end - start,
            header=None, usecols=[6], encoding="utf-8-sig",
        )

        count = int((df[6] <= 4).sum())
        return count

    def run(self)->tuple[int,list,list,float]:
        """
        Returns the tuple of final_answer, chunkSizePerProcess, answerPerProcess, totalTimeTaken
        """
        start_time = time.perf_counter()
        workers = self.num_of_processes

        try:
            if not isinstance(workers, int):
                raise ValueError("The number of threads must be an integer.")

            if workers < 1:
                raise ValueError("There must be at least one thread.")

            if not isinstance(self.dataset_size, int) or self.dataset_size < 0:
                raise ValueError("The dataset size must be a nonnegative integer.")
            if not self.dataset_path or not os.path.exists(self.dataset_path):
                raise FileNotFoundError("Dataset not found: " + str(self.dataset_path))

        except Exception as error:
            error_message = str(error)
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            return error_message, [0], [0], elapsed

        
        chunk_sizes = []
        chunks=[]
        processes = []

        

        number_of_rows = self.dataset_size
        rows_per_thread = number_of_rows // workers
        leftover_rows = number_of_rows % workers
        start = 0

        for index in range(workers):
            chunk_size = rows_per_thread

            # Give one extra row to each of the first few threads.
            if index < leftover_rows:
                chunk_size = chunk_size + 1

            end = start + chunk_size
            chunk_sizes.append(chunk_size)

            chunk = (start, end)
            chunks.append(chunk)

            start = end

       
        try:
            with Pool(processes=workers) as pool:
                answers = pool.map(self.count_chunk, chunks)
        except Exception as error:
            return str(error), chunk_sizes, [], time.perf_counter() - start_time

        total = 0
        for answer in answers:
            total = total + answer

        end_time = time.perf_counter()
        elapsed = end_time - start_time

        return total, chunk_sizes, answers, elapsed
        raise NotImplementedError("Implement your logic here")



if __name__ == '__main__':
    DATA_PATH = os.getenv('PATH_DATASET')
    solution = MultiProcessingSolution(num_of_processes=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerProcess,answerPerProcess,totalTimeTaken = solution.run()
    print(final_answer, totalTimeTaken)
    print("Number of processes:", solution.num_of_processes)
    print("Rows assigned to each task:", chunkSizePerProcess)
    print("Answer from each task:", answerPerProcess)
    print("Total rows processed:", sum(chunkSizePerProcess))
    print("Sum of partial answers:", sum(answerPerProcess))
    print("Final answer:", final_answer)
    print("Time taken in seconds:", totalTimeTaken)

    if sum(answerPerProcess) == final_answer:
        print("CHECK PASSED: partial answers match the final answer.")
    else:
        print("CHECK FAILED: partial answers do not match the final answer.")

