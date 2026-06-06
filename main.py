# Not to be used yet, it's for final implementation, Used Ai for creation

import logging
import threading
import webview
from multiprocessing import Pool
from batch import create_batches
from ranker import process_batch, merge_results
from output_writer import write_output

# Set up logging — saves logs to a file and also prints them to the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/log/talentrank.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class API:
    # This is called by the frontend (index.html) when the user clicks "Start Ranking"
    def start_ranking(self, file_path):
        # Run the ranking in the background so the UI doesn't freeze
        thread = threading.Thread(target=self._run_ranking, args=(file_path,), daemon=True)
        thread.start()
        return "Ranking Started"

    def _run_ranking(self, file_path):
        try:
            # Step 1: Split the file into 4 batches
            batches = create_batches(file_path, num_batches=4)

            # Step 2: Score each batch in parallel using 4 worker processes
            with Pool(processes=4) as pool:
                results = pool.map(process_batch, batches)

            # Step 3: Merge all results and keep only the top 100
            top100 = merge_results(results, top_n=100)

            # Step 4: Save the top 100 to a CSV file
            write_output(top100, "output.csv")
            logger.info("Done — %d candidates saved to output.csv", len(top100))

        except FileNotFoundError:
            logger.error("File not found: %s", file_path)
        except Exception as e:
            logger.error("Ranking failed: %s", e, exc_info=True)


# Only run the app when this file is executed directly.
# This guard also prevents worker processes from accidentally
# opening extra windows when running on Windows/macOS.
if __name__ == "__main__":
    api = API()
    window = webview.create_window("TalentRank AI", "index.html", js_api=api)
    webview.start()