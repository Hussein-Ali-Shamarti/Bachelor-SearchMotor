import ollama

def rewrite_query(user_query):
    """
    Uses a local AI model (Mistral) to rewrite search queries for better accuracy.
    """
    try:
        # Call Ollama's chat model for query optimization
        response = ollama.chat(
            model="mistral", 
            messages=[
                {"role": "system", "content": "You are an AI that rewrites search queries to improve database search accuracy. Only return ONE optimized query without numbering."},
                {"role": "user", "content": f"Rewrite the search query: {user_query}"}
            ]
        )

        # Ensure the response contains the expected data
        if 'message' in response and 'content' in response['message']:
            # Extract the optimized query (first line of content)
            optimized_query = response['message']['content'].strip().split("\n")[0]
            return optimized_query
        else:
            print("Error: Unexpected response format:", response)
            return "Failed to generate optimized query."
    except Exception as e:
        print(f"Error in query rewriting: {e}")
        return "An error occurred while rewriting the query."

# Test it
if __name__ == "__main__":
    test_query = "AI in healthcare"
    optimized_query = rewrite_query(test_query)
    print("Optimized Query:", optimized_query)
