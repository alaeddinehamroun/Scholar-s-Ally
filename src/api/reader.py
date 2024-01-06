from haystack.nodes import FARMReader
readers = [
    "deepset/roberta-base-squad2",
    "deepset/xlm-roberta-base-squad2-distilled",
    "deepset/xlm-roberta-large-squad2",
    "deepset/minilm-uncased-squad2",
    "ahotrod/albert_xxlargev1_squad2_512"
    
]

# def get_reader(model_name_or_path="deepset/xlm-roberta-base-squad2-distilled"):
def get_reader(model_name_or_path="deepset/roberta-base-squad2"):

    """
    Get reader
    Args:
        model_name_or_path: model name or path
    Returns:
        reader: reader
    """
    
    reader = FARMReader(
        model_name_or_path=model_name_or_path, 
        use_gpu=True,
        
    )
    
    return reader
