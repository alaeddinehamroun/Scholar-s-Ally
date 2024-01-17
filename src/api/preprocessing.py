from haystack.nodes import PreProcessor, PDFToTextConverter
import logging
from haystack.utils import convert_files_to_docs


def convert_files(doc_dir):
    """
    Convert files in a directory to documents
    # Expected data format:
    # docs = [
    #     {
    #         'content': DOCUMENT_TEXT_HERE,
    #         'meta': {'name': DOCUMENT_NAME, ...}
    #     }, ...
    # ]
    
    Args:
        doc_dir: directory containing documents to be converted
    Returns:
        docs: list of converted documents
    """
    
    try:
        logging.info("Converting files to docs")
        all_docs = convert_files_to_docs(dir_path=doc_dir)

        logging.info(f"Finished converting {len(all_docs)} files ")
        return all_docs
    
    except Exception as e:
        logging.error(f"Error converting files: {e}")
        raise e

def get_preprocessor():

    """
    Get preprocessor
    

    Returns:
        preprocessor: preprocessor
    """
    
    preprocessor = PreProcessor(
            # Cleaning
            clean_empty_lines=True, # Will normalize 3 or more consecutive empty lines to be just a two empty lines
            clean_whitespace=True, # Will remove any whitespace at the begining or end of each line in the text
            clean_header_footer=True, # Will remove any long header or footer texts that are repeated on each page
            
            # Splitting: using sliding window approach
            split_by='word', # The unit by which you want to split the documents
            split_overlap=20, # Enables the sliding window approach
            split_length=100, # The max number of words in a document
            split_respect_sentence_boundary=True, # Retains complete sentences in split documents
            language='en', # Used by NLTK to best detect the sentence boundaries for that language
            # add_page_number=True, # Adds page numbers to the meta fields of the documents
        )
    return preprocessor

def get_converter():
    return PDFToTextConverter(
        remove_numeric_tables=True, # If True, tables containing numbers only will be removed from the docs
        valid_languages=["fr", "en"], # Only considers text in these languages
    )

def preprocess(docs):
    """
    Preprocess documents in a directory
    
    Args:
        doc_dir: directory containing documents to be preprocessed
    Returns:
        docs: list of preprocessed documents
    """
    
    # Preprocessing
    try:
        preprocessor = get_preprocessor()
        docs = preprocessor.process(docs)

        return docs
    except Exception as e:
        logging.error(f"Error preprocessing files: {e}")
