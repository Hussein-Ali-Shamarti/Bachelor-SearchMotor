import React, { useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners";
import './SearchPage.css'; 

const SearchPage = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [visibleResults, setVisibleResults] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedArticle, setSelectedArticle] = useState(null);

  const generateEmbedding = async (query) => {
    try {
      const response = await axios.post("http://127.0.0.1:5001/generate-embedding", { text: query });
      return response.data.embedding;
    } catch (error) {
      console.error("Embedding API Error:", error);
      return [];
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setResults([]);
    setVisibleResults(5);
    setSelectedArticle(null);

    const embedding = await generateEmbedding(query);

    try {
      const response = await axios.post("http://127.0.0.1:5001/ai-search", {
        embedding: embedding,
        k: 50, 
      });

      if (response.data.error) {
        setError(response.data.error);
        return;
      }

      if (Array.isArray(response.data) && response.data.length > 0) {
        setResults(response.data);
      } else {
        setError("No relevant articles found.");
      }
    } catch (err) {
      setError("Failed to fetch results. Make sure Flask is running.");
      console.error(err);
    }
    setLoading(false);
  };

  const loadMoreResults = () => {
    setVisibleResults((prev) => prev + 10);
  };

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
          {results.length === 0 ? (
            <p>No results found.</p>
          ) : (
            <ul>
              {results.map((article, index) => (
                <li
                  key={index}
                  className="result-item"
                  onClick={() => setSelectedArticle(article)}
                >
                  <h4>{article.title || "No Title Available"}</h4>
                  <p><strong>Author(s):</strong> {article.author || "Unknown"}</p>
                  <p><strong>Abstract:</strong> {article.abstract.substring(0, 100)}...</p>
                </li>
              ))}
            </ul>
          )}
        </div>
  
        {/* Article Details (Shown when selected) */}
        {selectedArticle && (
          <div className="selected-article-container">
            <h2>Article Details</h2>
            <p><strong>Title:</strong> {selectedArticle.title || "N/A"}</p>
            <p><strong>ISBN:</strong> {selectedArticle.isbn || "N/A"}</p>
            <p><strong>Author(s):</strong> {selectedArticle.author || "Unknown"}</p>
            <p><strong>Publication Date:</strong> {selectedArticle.publication_date || "N/A"}</p>
            {selectedArticle.pdf_url && (
              <p>
                <strong>PDF URL:</strong>{" "}
                <a href={selectedArticle.pdf_url} target="_blank" rel="noopener noreferrer">
                  View PDF
                </a>
              </p>
            )}
            <p><strong>Keywords:</strong> {selectedArticle.keywords ? selectedArticle.keywords.join(", ") : "None"}</p>
            <p><strong>Abstract:</strong> {selectedArticle.abstract}</p>
  
            <button onClick={() => setSelectedArticle(null)} className="back-button">
              Back to Results
            </button>
          </div>
        )}
      </div>
    </div>
  );
}  

export default SearchPage;
