import React, { useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners";
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

  // Generate embedding for the search query
  const generateEmbedding = async (query) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5001/generate-embedding", // Corrected URL
        { text: query }
      );
      return response.data.embedding;
    } catch (error) {
      console.error("Embedding API Error:", error);
      setError("Failed to generate embedding. Please try again.");
      return null;
    }
  };

  // Fetch the summary of the selected article
  const fetchArticleSummary = async (articleId) => {
    try {
      setSummaryLoading(true);
      console.log(`Fetching summary for article ID: ${articleId}`);

      const response = await axios.get(
        `http://127.0.0.1:5001/article-summary/${articleId}` // Correct URL here
      );

      // Debugging: Log the response from the server
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
      setArticleSummary("Error fetching summary.");
    } finally {
      setSummaryLoading(false);
    }
  };

  // Handle the search functionality
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

    const embedding = await generateEmbedding(query);
    if (!embedding) {
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5001/ai-search", {
        // Corrected URL
        embedding,
        k: 50
      });

      if (response.data.error) {
        setError(response.data.error);
      } else if (Array.isArray(response.data) && response.data.length > 0) {
        setResults(response.data);
      } else {
        setError("No relevant articles found.");
      }
    } catch (err) {
      setError("Failed to fetch results. Ensure Flask server is running.");
      console.error("Search API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Load more results on button click
  const loadMoreResults = () => setVisibleResults((prev) => prev + 10);

  return (
    <div className="search-page-container">
      <h1>AI-Powered Search</h1>

      {/* Search Input */}
      <div className="search-section">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter search query..."
          className="search-input"
        />
        <button onClick={handleSearch} className="search-button">
          Search
        </button>
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="loading-spinner">
          <ClipLoader size={50} color={"#123abc"} loading={loading} />
        </div>
      )}

      {/* Error Message */}
      {error && <p className="error-message">{error}</p>}

      {/* Results & Selected Article Side by Side */}
      <div className="results-container">
        {/* Scrollable Results List */}
        <div className="results-list">
          {results.length === 0 && !loading ? (
            <p>No results found.</p>
          ) : (
            <ul>
              {results.slice(0, visibleResults).map((article) => (
                <li
                  key={article.id}
                  className={`result-item ${
                    selectedArticle?.id === article.id ? "selected" : ""
                  }`}
                  onClick={() => {
                    if (selectedArticle?.id !== article.id) {
                      setSelectedArticle(article);
                      setArticleSummary(""); // Clear previous summary
                      fetchArticleSummary(article.id);
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
            </div>

            <button
              onClick={() => setSelectedArticle(null)}
              className="back-button"
            >
              Back to Results
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
