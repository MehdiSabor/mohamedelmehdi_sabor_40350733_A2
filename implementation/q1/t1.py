"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.
"""
# import threading
import pandas as pd
from threading import Thread
import time
from dotenv import load_dotenv
import os
load_dotenv()

class ThreadingSolution:
    """
    You are allowed to implement as many helper methods and variables as you wish 
    """
    def __init__(self, num_of_threads=None, dataset_path=None, dataset_size=None):
        self.num_of_threads = num_of_threads
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size

    def count_chunk(self, chunk, answers, index):
        start, end = chunk
        try:
            if start == end:
                answers[index] = 0
                return

            df = pd.read_csv(
                self.dataset_path, skiprows=1 + start, nrows=end - start,
                header=None, usecols=[6], encoding="utf-8-sig",
            )

            count = int((df[6] <= 4).sum())
            answers[index] = count
        except Exception as error:
            answers[index] = error

    def run(self) ->tuple[int,list,list,float]:
        """
        Returns the tuple of final_answer, chunkSizePerThread, answerPerThread, totalTimeTaken. eg., (3, [5,5,5], [1,2,3], 12.5)
        """

        start_time = time.perf_counter()
        workers = self.num_of_threads

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

        answers = []
        chunk_sizes = []
        threads = []

        for index in range(workers):
            answers.append(0)

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
            thread = Thread(
                target=self.count_chunk,
                args=(chunk, answers, index),
            )
            threads.append(thread)

            start = end

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        for answer in answers:
            if isinstance(answer, Exception):
                return str(answer), chunk_sizes, [], time.perf_counter() - start_time

        total = 0
        for answer in answers:
            total = total + answer

        end_time = time.perf_counter()
        elapsed = end_time - start_time

        return total, chunk_sizes, answers, elapsed


if __name__ == '__main__':
    DATA_PATH = os.getenv('PATH_DATASET')
    if DATA_PATH is None:
        raise Exception("No data path found! Please set up .env file.")
    
    solution = ThreadingSolution(num_of_threads=4, dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken = solution.run()
    print(final_answer, totalTimeTaken)

