import os
import dask
from dask import delayed

# Function to be executed by each worker
def worker():
    # Get process id
    process_id = os.getpid()
    # Create a large list
    large_list = list(range(7000))
    return process_id, large_list

if __name__ == "__main__":
    # Create Dask delayed objects for each worker function call
    delayed_workers = [delayed(worker)() for _ in range(3)]

    # Compute delayed objects in parallel using multiprocessing scheduler
    results = dask.compute(*delayed_workers, scheduler='processes')

    # Print results
    for result in results:
        process_id, result_list = result
        print(f"Received list from worker {process_id}, length: {len(result_list)}")
