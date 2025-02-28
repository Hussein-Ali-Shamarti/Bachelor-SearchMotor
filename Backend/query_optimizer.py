import openai

# Initialize the OpenAI client with your API key
openai.api_key = 'your_openai_api_key_here'

def rewrite_query(user_query):
    """
    Uses OpenAI's GPT model to rewrite search queries for better accuracy.
    """
    try:
        # Call OpenAI's GPT model for query optimization
        response = openai.Completion.create(
            model="gpt-4",  # Choose the model based on availability or preferences
            prompt=f"Rewrite the following search query for better accuracy: {user_query}",
            max_tokens=100,  # Limit the output size to a reasonable length
            temperature=0.7  # Controls randomness; you can adjust this based on your needs
        )

        # Extract the optimized query from the response
        optimized_query = response.choices[0].text.strip()
        return optimized_query

    except Exception as e:
        print(f"Error in query rewriting: {e}")
        return "An error occurred while rewriting the query."

# Test the function
if __name__ == "__main__":
    test_query = "AI in healthcare"
    optimized_query = rewrite_query(test_query)
    print("Optimized Query:", optimized_query)
