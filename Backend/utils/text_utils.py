def split_text_into_chunks(text, max_completion_tokens=3000):
    """
    Split text into smaller chunks based on sentences 
    to avoid cutting off mid-sentence.
    """
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    
    for sentence in sentences:
        current_chunk.append(sentence)
        # Rough estimate: 1 token ≈ 4 characters
        if len(' '.join(current_chunk)) * 4 > max_completion_tokens:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = []
    
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return chunks

def truncate_text(text, max_tokens, encoding):
    """
    Truncates the given text to at most max_tokens tokens using 
    the provided tiktoken encoding.
    """
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)
