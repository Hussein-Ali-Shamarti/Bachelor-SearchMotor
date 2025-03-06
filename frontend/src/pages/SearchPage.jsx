import React, { useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners";
import Enter from "../Pictures-icones/Eenter.svg";
import "./SearchPage.css";

const SearchPage = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [visibleResults, setVisibleResults] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleSummary, setArticleSummary] = useState("");
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [embedding, setEmbedding] = useState(null);

  // Chat state
  const [showChat, setShowChat] = useState(false);
  const [chatMessage, setChatMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);

  // Backend URL from environment variable
  const backendUrl =
    process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:5001";

  // Generate embedding for the search query
  const generateEmbedding = async (query) => {
    try {
      const response = await axios.post(`${backendUrl}/generate-embedding`, {
        text: query
      });
      return response.data.embedding;
    } catch (error) {
      console.error("Embedding API Error:", error);
      setError(
        "Failed to generate embedding. Please check your connection or try again later."
      );
      return null;
    }
  };

  // Fetch the summary of the selected article
  const fetchArticleSummary = async (articleId) => {
    try {
      setSummaryLoading(true);
      console.log(`Fetching summary for article ID: ${articleId}`);

      const response = await axios.get(
        `${backendUrl}/article-summary/${articleId}?generate=true`
      );

      console.log("Summary Response:", response.data);

      if (
        response.data.summary &&
        response.data.summary !== "Failed to generate summary."
      ) {
        setArticleSummary(response.data.summary);
      } else {
        setArticleSummary("Failed to generate summary.");
      }
    } catch (err) {
      console.error("Failed to fetch article summary:", err);
      setArticleSummary("Error fetching summary. Please try again.");
    } finally {
      setSummaryLoading(false);
    }
  };

  // Extract location filter from the query using regex.
  // This regex looks for "from <location>" (location can include letters, spaces, commas)
  const extractLocationFilter = (text) => {
    const match = text.toLowerCase().match(/from\s+([a-z\s,]+)/);
    if (match && match[1]) {
      return match[1].trim();
    }
    return "";
  };

  // Handle search functionality using a single searchbar.
  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Please enter a search query.");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);
    setVisibleResults(5);
    setSelectedArticle(null);
    setArticleSummary("");
    setShowChat(false);
    setChatHistory([]);
    setEmbedding(null);

    // Generate the embedding
    const emb = await generateEmbedding(query);
    if (!emb) {
      setLoading(false);
      return;
    }
    setEmbedding(emb);

    // Extract location filter from the query (if any)
    const locationFilter = extractLocationFilter(query);

    try {
      const payload = {
        query, // the original query text
        embedding: emb,
        k: 50
      };
      // Pass the location filter if one was extracted.
      if (locationFilter) {
        payload.location = locationFilter;
      }

      const response = await axios.post(`${backendUrl}/ai-search`, payload);

      if (response.data.error) {
        setError(response.data.error);
      } else if (Array.isArray(response.data) && response.data.length > 0) {
        setResults(response.data);
      } else {
        setError("No relevant articles found.");
      }
    } catch (err) {
      setError(
        "Failed to fetch results. Ensure the backend server is running."
      );
      console.error("Search API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Load more results on button click
  const loadMoreResults = () => setVisibleResults((prev) => prev + 10);

  // Handle sending a chat message
  const sendChatMessage = async () => {
    if (!chatMessage.trim() || !selectedArticle || !embedding) return;

    // Append user message to chat history
    const newHistory = [
      ...chatHistory,
      { sender: "user", message: chatMessage }
    ];
    setChatHistory(newHistory);
    setChatMessage("");
    setChatLoading(true);

    try {
      const response = await axios.post(`${backendUrl}/chat`, {
        embedding: embedding,
        article_id: selectedArticle.id,
        message: chatMessage,
        k: 50
      });

      if (response.data.error) {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: "Error: " + response.data.error }
        ]);
      } else {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: response.data.answer }
        ]);
      }
    } catch (err) {
      console.error("Chat API Error:", err);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", message: "Failed to send message. Please try again." }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  // Function to handle pressing Enter key
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="search-page-container">
      <h1>AI-Powered Search</h1>

      {/* Search Input */}
      <div className="search-section">
        <h1 style={{ fontSize: "120%" }}> What can I help you with?</h1>
        <div className="search-box">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter search query..."
            className="search-input"
          />
          <button type="button" onClick={handleSearch} className="Enter-icon">
            <img src={Enter} alt="Enter Icon" />
          </button>
        </div>
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="loading-spinner">
          <ClipLoader size={50} color={"#123abc"} loading={loading} />
        </div>
      )}

      {/* Error Message */}
      {error && <p className="error-message">{error}</p>}

      {/* Main Content Area */}
      <div className="content-container">
        {/* Results List */}
        <div className="results-container">
          {results.length === 0 && !loading ? (
            <p>No results found.</p>
          ) : (
            <ul className="results-list">
              {results.slice(0, visibleResults).map((article) => (
                <li
                  key={article.id}
                  className={`result-item ${
                    selectedArticle?.id === article.id ? "selected" : ""
                  }`}
                  onClick={() => {
                    if (selectedArticle?.id !== article.id) {
                      setSelectedArticle(article);
                      setArticleSummary("");
                      setShowChat(false);
                      setChatHistory([]);
                    }
                  }}
                >
                  <h4>{article.title || "No Title Available"}</h4>
                  <p>
                    <strong>Author(s):</strong> {article.author || "Unknown"}
                  </p>
                  <p>
                    <strong>Abstract:</strong>{" "}
                    {article.abstract
                      ? article.abstract.substring(0, 100) + "..."
                      : "No abstract available."}
                  </p>
                </li>
              ))}
            </ul>
          )}

          {/* Load More Button */}
          {results.length > visibleResults && (
            <button onClick={loadMoreResults} className="load-more-button">
              Load More
            </button>
          )}
        </div>

        {/* Article Details */}
        {selectedArticle && (
          <div className="selected-article-container">
            <h2>Article Details</h2>
            <p>
              <strong>Title:</strong> {selectedArticle.title || "N/A"}
            </p>
            <p>
              <strong>ISBN:</strong> {selectedArticle.isbn || "N/A"}
            </p>
            <p>
              <strong>Author(s):</strong> {selectedArticle.author || "Unknown"}
            </p>
            <p>
              <strong>Publication Date:</strong>{" "}
              {selectedArticle.publication_date || "N/A"}
            </p>

            {/* Display Conference Information if available */}
            {selectedArticle.conference_name && (
              <p>
                <strong>Conference:</strong> {selectedArticle.conference_name}
              </p>
            )}
            {selectedArticle.conference_location && (
              <p>
                <strong>Conference Location:</strong>{" "}
                {selectedArticle.conference_location}
              </p>
            )}
            {selectedArticle.conference_articles &&
              selectedArticle.conference_articles.length > 0 && (
                <div>
                  <strong>Conference Version:</strong>
                  <ul>
                    {selectedArticle.conference_articles.map((version, idx) => (
                      <li key={idx}>{version}</li>
                    ))}
                  </ul>
                </div>
              )}

            {/* PDF URL */}
            {selectedArticle.pdf_url && (
              <p>
                <strong>PDF URL:</strong>{" "}
                <a
                  href={selectedArticle.pdf_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View PDF
                </a>
              </p>
            )}

            <p>
              <strong>Keywords:</strong>{" "}
              {selectedArticle.keywords
                ? selectedArticle.keywords.join(", ")
                : "None"}
            </p>
            <p>
              <strong>Abstract:</strong>{" "}
              {selectedArticle.abstract || "No abstract available."}
            </p>

            {/* Article Summary */}
            <div className="article-summary">
              <h3>Summary</h3>
              {summaryLoading ? (
                <ClipLoader
                  size={30}
                  color={"#123abc"}
                  loading={summaryLoading}
                />
              ) : (
                <p>{articleSummary || "No summary available."}</p>
              )}
              {!articleSummary && !summaryLoading && (
                <button
                  onClick={() => fetchArticleSummary(selectedArticle.id)}
                  className="generate-summary-button"
                >
                  Generate Summary
                </button>
              )}
            </div>

            <button
              onClick={() => setSelectedArticle(null)}
              className="back-button"
            >
              Back to Results
            </button>
          </div>
        )}

        {/* Chat Section */}
        {selectedArticle && (
          <div className="chat-section">
            <button
              onClick={() => setShowChat((prev) => !prev)}
              className="chat-toggle-button"
            >
              {showChat ? "Back to article" : "Chat with AI"}
            </button>
            {showChat && (
              <div className="chat-container">
                <h3>Chat about this article</h3>
                <div className="chat-history">
                  {chatHistory.length === 0 && (
                    <p>No messages yet. Start the conversation!</p>
                  )}
                  {chatHistory.map((entry, index) => (
                    <div
                      key={index}
                      className={`chat-message ${
                        entry.sender === "user" ? "user-message" : "bot-message"
                      }`}
                    >
                      <strong>
                        {entry.sender === "user" ? "You:" : "Bot:"}
                      </strong>{" "}
                      {entry.message}
                    </div>
                  ))}
                </div>
                <div className="chat-input-container">
                  <input
                    type="text"
                    value={chatMessage}
                    onChange={(e) => setChatMessage(e.target.value)}
                    placeholder="Type your message..."
                    className="chat-input"
                  />
                  <button
                    onClick={sendChatMessage}
                    className="send-chat-button"
                    disabled={chatLoading}
                  >
                    {chatLoading ? (
                      <ClipLoader
                        size={15}
                        color={"#fff"}
                        loading={chatLoading}
                      />
                    ) : (
                      "Send"
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
