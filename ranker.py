#ranks candidates based on their scores and returns the top 500 candidates per batch

from multiprocessing import Pool
import heapq


from batch import create_batches
from score_computer import score

def process_batch(batch):
    
    top500 = []
    
    for candidate in batch:
        
        candidate_score = score(candidate)
        
        if len(top500) < 500:
            heapq.heappush(top500, (candidate_score, candidate))
        elif candidate_score > top500[0][0]:
            heapq.heappushpop(top500, (candidate_score, candidate))
            
    return top500


def run_ranking(file_path):
    
    batches = create_batches(file_path, num_batches=4)
    
    with Pool(processes=4) as pool:
        results = pool.map(process_batch, batches)
    
    
    return merge_results(results)


def merge_results(batch_results, top_n=100):
    
    merged = sorted(
    
        (item for batch in batch_results for item in batch),
        key=lambda x: x[0],
        reverse=True,
    )
    
    return merged[:top_n]




#multiprocessing safety guard, prevents infinite spawning of processes on Windows

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    top100 = run_ranking(sys.argv[1])
    print(f"Top {len(top100)} candidates ranked successfully.")
 
