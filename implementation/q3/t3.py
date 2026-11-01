"""
You are allowed use necessary python libraries.
You are not allowed to have any global function or variables.
"""
from dotenv import load_dotenv
import os
load_dotenv()
import pandas as pd
import time

from mpi4py import MPI

class MPISolution:
    """
    You are allowed to implement as many methods and variables as you wish
    """
    def __init__(self, dataset_path=None, dataset_size=None):
        self.dataset_path = dataset_path
        self.dataset_size = dataset_size

    def read_rows(self, start, end):
        if start == end:
            return pd.DataFrame()

        df = pd.read_csv(
                self.dataset_path, skiprows=1 + start, nrows=end - start,
                header=None, usecols=[3, 6, 0, 4], encoding="utf-8-sig",
                dtype={0: str, 3: str},
            )
        return df

    def group_chunk(self, df):
        if len(df) == 0:
            return {}

        users = {}
        for user_id, score, book_id, u_name in zip(df[3], df[6], df[0],df[4]):
                if pd.isna(user_id) or pd.isna(score):
                    continue
                if user_id not in users:
                    users[user_id] = [0.0, 0, set(),set()]
                users[user_id][0] = users[user_id][0] + score
                users[user_id][1] = users[user_id][1] + 1
                users[user_id][2].add(book_id)
                if pd.notna(u_name):
                    users[user_id][3].add(u_name)

        return users

    def run(self)->tuple[int,list,list,float]:
        """
        Returns the tuple of computed result and time taken. eg., ("I am final Result", 3.455)
        """

        start_time = time.perf_counter()

        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        workers = comm.Get_size()

        error_message = None
        data = None
        if rank == 0:
            try:
                if not isinstance(self.dataset_size, int) or self.dataset_size < 0:
                    raise ValueError("The dataset size must be a nonnegative integer.")
                if not self.dataset_path or not os.path.exists(self.dataset_path):
                    raise FileNotFoundError("Dataset not found: " + str(self.dataset_path))
                # Only the master reads the dataset, the workers get their rows from it
                data = self.read_rows(0, self.dataset_size)
            except Exception as error:
                error_message = str(error)
            for worker in range(1, workers):
                comm.send(error_message, dest=worker)
        else:
            error_message = comm.recv(source=0)
        if error_message is not None:
            return error_message, [0], [0], time.perf_counter() - start_time

        chunk_sizes = []
        chunks = None
        chunk = None
        if rank == 0:
            # Rank 0 only distributes and aggregates, unless it runs alone
            if workers > 1:
                worker_ranks = list(range(1, workers))
            else:
                worker_ranks = [0]
            chunks = {}
            number_of_rows = self.dataset_size
            rows_per_process = number_of_rows // len(worker_ranks)
            leftover_rows = number_of_rows % len(worker_ranks)
            start = 0
            for index, worker in enumerate(worker_ranks):
                chunk_size = rows_per_process
                if index < leftover_rows:
                    chunk_size = chunk_size + 1
                end = start + chunk_size
                chunk_sizes.append(chunk_size)
                chunks[worker] = data.iloc[start:end]
                start = end

            chunk = chunks.get(0)
            for worker in range(1, workers):
                comm.send(chunks[worker], dest=worker)
        else:
            chunk = comm.recv(source=0)
        part = None
        error_message = None
        if chunk is not None:
            try:
                part = self.group_chunk(chunk)
            except Exception as error:
                error_message = str(error)

        if rank != 0:
            comm.send((part, error_message), dest=0)
            return None, [], [], time.perf_counter() - start_time

        if rank == 0:
            answers = []
            errors = []
            if chunk is not None:
                answers.append(part)
                errors.append(error_message)
            for worker in range(1, workers):
                worker_part, worker_error = comm.recv(source=worker)
                answers.append(worker_part)
                errors.append(worker_error)

            for error_message in errors:
                if error_message is not None:
                    return error_message, chunk_sizes, [], time.perf_counter() - start_time

            merged = {}

            for users in answers:
                for user_id in users:
                    score_sum, count, unique_books, name = users[user_id]

                    if user_id not in merged:
                        merged[user_id] = [0.0, 0, set(),set()]

                    merged[user_id][0] = merged[user_id][0] + score_sum
                    merged[user_id][1] = merged[user_id][1] + count
                    merged[user_id][2].update(unique_books)
                    merged[user_id][3].update(name)

            
            max_count = -1
            winning_users = []

            for user_id in merged:
                score_sum, n, unique_books, names = merged[user_id]

                if score_sum / n == 4:
                    book_count = len(unique_books)
                    user_info = {
                        
                        "names": names,
                    }

                    if book_count > max_count:
                        max_count = book_count
                        winning_users = [user_info]

                    elif book_count == max_count:
                        winning_users.append(user_info)
            
                

            elapsed = time.perf_counter() - start_time
            return winning_users, chunk_sizes, answers, elapsed


        return None, [], [], time.perf_counter() - start_time


if __name__ == '__main__':
    DATA_PATH = os.getenv('PATH_DATASET')
    solution = MPISolution(dataset_path=DATA_PATH, dataset_size=3000000)
    final_answer,chunkSizePerThread,answerPerThread,totalTimeTaken = solution.run()

    if MPI.COMM_WORLD.Get_rank() == 0:
        print({
            "final_answer": final_answer,
            "chunkSizePerThread": chunkSizePerThread,
            "answerPerThread": answerPerThread,
            "totalTimeTaken": totalTimeTaken
        })

     
