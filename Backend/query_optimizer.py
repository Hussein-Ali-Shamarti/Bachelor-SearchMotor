import ollama

def rewrite_query(user_query):
    """
    Uses a local AI model (Mistral) to rewrite search queries for better accuracy.
    """
    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": "You are an AI that rewrites search queries to improve database search accuracy. Only return ONE optimized query without numbering."},
        {"role": "user", "content": f"Rewrite the search query: {user_query}"}
    ])
    
    # Extract the optimized query (first line)
    optimized_query = response['message']['content'].strip().split("\n")[0]
    
    return optimized_query

# Test it
if __name__ == "__main__":
    test_query = "AI in healthcare"
    optimized_query = rewrite_query(test_query)
    print("Optimized Query:", optimized_query)
