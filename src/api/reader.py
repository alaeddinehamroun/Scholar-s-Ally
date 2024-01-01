from haystack.nodes import FARMReader


def get_reader(model_name_or_path="deepset/xlm-roberta-base-squad2-distilled"):
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
