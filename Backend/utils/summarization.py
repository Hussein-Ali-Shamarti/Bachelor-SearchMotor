import openai
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils.text_utils import token_count, split_text_into_chunks

MODEL_NAME = "gpt-4-turbo"
MAX_TOKENS_PER_SUMMARY = 600
MAX_WORKERS = 10
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

async def summarize_full_text(text):
    loop = asyncio.get_event_loop()

    def call_openai():
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional academic summarizer."},
                {"role": "user", "content": f"""
                  Summarize the following academic paper in 6–7 clear and self-contained sentences.
                  Begin by stating the paper's objective and proposed contribution. 
                  Then explain the framework or methods introduced, how they are structured, and any evaluation or findings.
                  Include key limitations or criticisms noted by the author. 
                  If applicable, describe implications for future citizen-centric service design, such as open data. 
                  Use formal academic language and ensure that all information is accurate and non-redundant.
                  
                  Text:
                  {text}
                  """}
            ],
            max_tokens=MAX_TOKENS_PER_SUMMARY,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    return await loop.run_in_executor(executor, call_openai)

async def summarize_chunk(chunk):
    loop = asyncio.get_event_loop()

    def call_openai():
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional academic summarizer."},
                {"role": "user", "content": f"""
                 Summarize the following academic section in 5 to 7 self-contained sentences. 
                 Start with the purpose, describe the framework or contributions, and mention key findings or limitations.
                 Use clear academic language and ensure continuity.
                 
                 Text:
                 {chunk}
                 """}
            ],
            max_tokens=MAX_TOKENS_PER_SUMMARY,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    return await loop.run_in_executor(executor, call_openai)

async def summarize_with_openai(text, abstract_length, chunk_token_size=800):
    try:
        if token_count(text, model=MODEL_NAME) < 10000:
            print("Using full-text summarization...")
            return await summarize_full_text(text)

        print("Text too long. Falling back to chunked summarization...")
        chunks = split_text_into_chunks(text, max_tokens=chunk_token_size, model=MODEL_NAME)
        tasks = [summarize_chunk(chunk) for chunk in chunks]
        summaries = await asyncio.gather(*tasks)

        final_summary = " ".join(summaries)
        return final_summary.strip()

    except Exception as e:
        print(f"Error in summarize_with_openai: {e}")
        return "Failed to generate summary."

# Backward compatibility alias
summarize_with_openai_async = summarize_with_openai
