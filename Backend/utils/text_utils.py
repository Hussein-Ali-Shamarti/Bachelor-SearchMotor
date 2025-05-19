# Dette skriptet tilbyr verktøy for å håndtere tekst i henhold til tokenbegrensninger 
# for GPT-modeller. Det inkluderer funksjoner for å telle tokens, trunkere tekst og 
# dele opp lange tekster i tokensikre tekstbolker.


import tiktoken

def token_count(text, model="gpt-4-turbo"):
    """
    Returns the number of tokens in a text using the tokenizer for the specified model.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def truncate_text(text, max_tokens, model="gpt-4-turbo"):
    """
    Truncate text to a maximum number of tokens using the specified model's tokenizer.
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)

def split_text_into_chunks(text, max_tokens=800, model="gpt-4-turbo"):
    """
    Splits text into chunks using actual token counts to avoid mid-sentence cuts and token overruns.
    
    This is primarily a fallback mechanism when full-text summarization exceeds the model context window.
    """
    encoding = tiktoken.encoding_for_model(model)
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        token_count = len(encoding.encode(sentence))

        if current_tokens + token_count > max_tokens:
            if current_chunk:
                chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentence]
            current_tokens = token_count
        else:
            current_chunk.append(sentence)
            current_tokens += token_count

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

    return chunks
