def text_after_prefix(prefix, text: str):
    return text.partition(prefix)[2].strip()
