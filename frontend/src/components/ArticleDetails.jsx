import React, { useState } from "react";
import axios from "axios";

const ArticleDetails = ({ selectedArticle, onOpenChat }) => {
  const [showSummary, setShowSummary] = useState(false);
  const [summary, setSummary] = useState("");
  const [summaryLoading, setSummaryLoading] = useState(false);

  const handleSummarize = async () => {
    if (!selectedArticle) return;
    setShowSummary(true);
    setSummaryLoading(true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:5001/article-summary/${selectedArticle.id}?generate=true`
      );
      if (response.data.summary) {
        setSummary(response.data.summary);
      } else {
        setSummary("Failed to generate summary.");
      }
    } catch (err) {
      console.error(err);
      setSummary("Error fetching summary.");
    } finally {
      setSummaryLoading(false);
    }
  };

  return (
    <section className="dashboard-cards">
      <div
        className={`selected-article-card ${
          showSummary ? "half-width" : "full-width"
        }`}
      >
        <div className="card-content">
          {selectedArticle ? (
            <>
              <h2>Article Details</h2>
              <p>
                <strong>Title:</strong> {selectedArticle.title || "N/A"}
              </p>
              <p>
                <strong>ISBN:</strong> {selectedArticle.isbn || "N/A"}
              </p>
              <p>
                <strong>Author(s):</strong>{" "}
                {(selectedArticle.author || "Unknown Author").trim()}
              </p>
              <p>
                <strong>Publication Date:</strong>{" "}
                {selectedArticle.publication_date || "N/A"}
              </p>

              {selectedArticle.conference_name && (
                <p>
                  <strong>Conference:</strong>{" "}
                  {selectedArticle.conference_name}
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
                      {selectedArticle.conference_articles.map(
                        (version, idx) => (
                          <li key={idx}>{version}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}

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
                  ? Array.isArray(selectedArticle.keywords)
                    ? selectedArticle.keywords.join(", ")
                    : selectedArticle.keywords
                  : "None"}
              </p>
              <p>
                <strong>Abstract:</strong>{" "}
                {selectedArticle.abstract || "No abstract available."}
              </p>

              <div className="button-wrapper">
                <button
                  className="summarize-button"
                  onClick={handleSummarize}
                >
                  Summarize
                </button>
                {onOpenChat && (
                    <button
                    className="chat-button"
                    onClick={onOpenChat}
                    >
                    Chat about this article
                    </button>
                )}
              </div>
            </>
          ) : (
            <>
              <h2>No article selected</h2>
              <p>Please select an article from the list.</p>
            </>
          )}
        </div>
      </div>

      {showSummary && (
        <div className="summary-article-card half-width">
          <button
            className="close-summary"
            onClick={() => setShowSummary(false)}
          >
            &times;
          </button>
          <div className="card-content">
            <h2>AI Summary</h2>
            {summaryLoading ? (
              <p>Loading summary...</p>
            ) : (
              <p>{summary || "No summary available."}</p>
            )}
          </div>
        </div>
      )}
    </section>
  );
};

export default ArticleDetails;
