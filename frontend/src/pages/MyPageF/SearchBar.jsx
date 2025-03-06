import React, { useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners";
import Enter from "../../assets/images/Enter.svg";
import "../../assets/styles/MyPageF/SearchBar.css"; 

const SearchPage = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [visibleResults, setVisibleResults] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleSummary, setArticleSummary] = useState(""); // Holds the summary text
  const [summaryLoading, setSummaryLoading] = useState(false);

  const generateEmbedding = async (query) => {
    try {
      const response = await axios.post("http://127.0.0.1:5001/generate-embedding", { text: query });
      return response.data.embedding;
    } catch (error) {
      console.error("Embedding API Error:", error);
      return [];
    }
  };

  // New function to fetch article summary from our backend endpoint
  const fetchArticleSummary = async (articleId) => {
    try {
      setSummaryLoading(true);
      const response = await axios.get(`http://127.0.0.1:5001/article-summary/${articleId}`);
      if (response.data.summary) {
        setArticleSummary(response.data.summary);
      }
    } catch (err) {
      console.error("Failed to fetch article summary", err);
    } finally {
      setSummaryLoading(false);
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setResults([]);
    setVisibleResults(5);
    setSelectedArticle(null);
    setArticleSummary("");
    
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

  // Function to handle pressing Enter key
  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="search-page-container">
      
  
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
            <img src={Enter} alt="Enter Icon"/>
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
                  onClick={() => {
                    setSelectedArticle(article);
                    setArticleSummary(""); // Clear any previous summary
                    // Immediately fetch the summary when the article is selected
                    fetchArticleSummary(article.id);
                  }}
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
  
            {/* Display the summary area */}
            <div className="article-summary">
              <h3>Summary</h3>
              {summaryLoading ? (
                <ClipLoader size={30} color={"#123abc"} loading={summaryLoading} />
              ) : articleSummary ? (
                <p>{articleSummary}</p>
              ) : (
                <p>No summary available.</p>
              )}
            </div>
  
            <button onClick={() => setSelectedArticle(null)} className="back-button">
              Back to Results
            </button>
          </div>
        )}
      </div>
      
    </div>
  );
};

export default SearchPage;
