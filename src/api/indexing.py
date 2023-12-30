import os
import logging
from preprocessing import convert_files, preprocess
if __name__ == '__main__':
    # This block runs only if the script is executed directly, not if imported.

    doc_dir = 'data/'

    try:
        logging.info("Running indexing separately")
        # files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
        # print(files_to_index)
        all_docs = convert_files(doc_dir)
        docs = preprocess(all_docs)
        logging.info("Finished running indexing")

    except Exception as e:
        logging.error(f"Error running indexing: {e}")
        raise e

