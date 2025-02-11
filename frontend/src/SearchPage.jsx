import React, { useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners"; // Import spinner component
import './SearchPage.css'; // Import the CSS file

const SearchPage = () => {
  const [query, setQuery] = useState(""); // User search query
  const [result, setResult] = useState(null); // Search result data
  const [loading, setLoading] = useState(false); // Loading state for search
  const [error, setError] = useState(""); // Error message if any

  const [chatHistory, setChatHistory] = useState([]); // Chat history state
  const [chatInput, setChatInput] = useState(""); // User's message for chat
  const [chatLoading, setChatLoading] = useState(false); // Loading state for chat

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    // Clear the chat history and input when a new search is performed
    setChatHistory([]); // Reset chat history
    setChatInput(""); // Clear the chat input

    try {
      const response = await axios.get(`http://127.0.0.1:5001/ai-search`, {
        params: { query },
      });

      console.log("Backend Response:", response.data); // Log the raw response

      setResult(response.data);
    } catch (err) {
      setError(
        "Failed to fetch results. Make sure Flask and Ollama are running."
      );
      console.error(err);
    }

    setLoading(false);
  };

  const handleChat = async () => {
    if (!chatInput.trim()) return;

    setChatLoading(true);
    setError("");

    try {
      const newChatHistory = [
        ...chatHistory,
        { role: "user", content: chatInput },
      ];

      const response = await axios.post(`http://127.0.0.1:5001/chat`, {
        message: chatInput,
        history: newChatHistory,
        context: result ? result.article.abstract : "", // Pass the context from the search result (article abstract)
      });

      console.log("Chat Response:", response.data);

      const aiMessage = {
        role: "assistant",
        content: response.data.response,
      };

      setChatHistory([...newChatHistory, aiMessage]);
    } catch (err) {
      setError(
        "Failed to send the message. Make sure Flask and Ollama are running."
      );
      console.error(err);
    }

    setChatLoading(false);
    setChatInput(""); // Clear chat input
  };

  return (
    <div className="search-page-container">
      <h1>AI-Powered Search & Chat</h1>

      {/* Search Section */}
      <div className="search-section">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter search query..."
          className="search-input"
        />
        <button
          onClick={handleSearch}
          className="search-button"
        >
          Search
        </button>

        {loading && (
          <div className="loading-spinner">
            <ClipLoader size={50} color={"#123abc"} loading={loading} />
          </div>
        )}
        {error && <p className="error-message">{error}</p>}

        {result && (
    <div className="result-container">
        <h3>Selected Article:</h3>
        <p><strong>Title:</strong> {result.article.title}</p>
        <p><strong>Abstract:</strong> {result.article.abstract}</p>
        <p><strong>Author(s):</strong> {result.article.author}</p>
        <p><strong>Publication Date:</strong> {result.article.publication_date}</p>

        <h3>AI Summary:</h3>
        <div className="ai-summary" dangerouslySetInnerHTML={{ __html: result.ai_summary }} />

        {result.article.pdf_url && (
            <div className="pdf-link-container">
                <h3>Download PDF:</h3>
                <a href={result.article.pdf_url} target="_blank" rel="noopener noreferrer">
                    Click here to download the PDF
                </a>
            </div>
        )}
    </div>
)}

      {/* Chat Section - Only visible when result is available */}
      {result && (
        <div className="chat-section">
          <h2>Chat with AI</h2>
          <div className="chat-container">
            {chatHistory.length === 0 && (
              <p style={{ textAlign: "center", color: "#aaa" }}>
                Start a conversation with the AI!
              </p>
            )}
            {chatHistory.map((entry, index) => (
              <div key={index} className="chat-history-entry">
                <strong>{entry.role === "user" ? "You" : "AI"}:</strong>
                <p style={{ margin: "5px 0" }}>{entry.content}</p>
              </div>
            ))}
          </div>

          <div className="chat-input-container">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Type your message..."
              className="chat-input"
            />
            <button
              onClick={handleChat}
              className="chat-send-button"
              disabled={chatLoading}
            >
              {chatLoading ? "Sending..." : "Send"}
            </button>
          </div>
        </div>
      )}
        </div>
    </div>
  );
};

export default SearchPage;
