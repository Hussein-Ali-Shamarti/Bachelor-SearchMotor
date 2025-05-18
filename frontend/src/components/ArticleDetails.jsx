import React, { useState, useEffect } from "react";
import axios from "axios";
import { FiCalendar, FiMapPin, FiUser, FiUsers  } from "react-icons/fi";
import { FaFilePdf } from "react-icons/fa";



const ArticleDetails = ({ selectedArticle, onOpenChat, onSearch, clearSelectedArticle, setQueryText }) => {
  const [showSummary, setShowSummary] = useState(false);
  const [summary, setSummary] = useState("");
  const [summaryLoading, setSummaryLoading] = useState(false);


  let authorList = [];
  let isMultipleAuthors = false;

  if (selectedArticle) {
    const rawAuthors = selectedArticle.author;
    authorList = Array.isArray(rawAuthors)
      ? rawAuthors
      : typeof rawAuthors === "string"
        ? rawAuthors.split(",").map((a) => a.trim())
        : [];
    isMultipleAuthors = authorList.length > 1;
  }

  useEffect(() => {
    setShowSummary(false);
    setSummary("");
    setSummaryLoading(false);
  }, [selectedArticle]);

  const handleSummarize = async () => {
    if (!selectedArticle) return;
    setShowSummary(true);
    setSummaryLoading(true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:5001/article-summary/${selectedArticle.id}?generate=true`
      );
      setSummary(response.data.summary || "Failed to generate summary.");
    } catch (err) {
      console.error(err);
      setSummary("Error fetching summary.");
    } finally {
      setSummaryLoading(false);
    }
  };


  const handleKeywordClick = (keyword) => {
  if (typeof clearSelectedArticle === "function") clearSelectedArticle();
  if (typeof setQueryText === "function") setQueryText(keyword);
  if (typeof onSearch === "function") onSearch(keyword);
};

  return (
    <section className="dashboard-cards">
      <div
        className={`selected-article-card full-width ${
          showSummary ? "" : "full-width"
        }`}
      >
        <div className="card-content">
          {selectedArticle ? (
            <>
              <h2>Article Details</h2>

              <h3 className="section-heading">{selectedArticle.title}</h3>
              <div><strong>ISBN:</strong> {selectedArticle.isbn}</div>
              <hr className="section-divider" />
              <div className="article-meta-row">
              <div className="meta-item">
                {selectedArticle.publication_date && (
                  <>
                    <FiCalendar className="icon-medium" />
                    <span>{selectedArticle.publication_date || "—"}</span>
                  </>
                )}
              </div>             
              <div className="meta-item author-wrap">
                {isMultipleAuthors ? (
                  <FiUsers className="icon-medium icon-authors" />
                ) : (
                  <FiUser className="icon-medium icon-authors" />
                )}
                <span className="authors-text">{selectedArticle.author || "—"}</span>
              </div>
              <div className="meta-item">
                {selectedArticle.conference_location && (
                  <>
                    <FiMapPin className="icon-medium" />
                    <span>{selectedArticle.conference_location || "—"}</span>
                  </>
                )}
              </div>
            </div>
           {selectedArticle.conference_name && (
                <div className="article-conference">
                  <strong>Conference:</strong> {selectedArticle.conference_name}
                </div>
              )}
              <hr className="section-divider" />

              {selectedArticle.pdf_url && (
                <a
                  href={selectedArticle.pdf_url}
                  download
                  target="_blank"
                  rel="noopener noreferrer"
                  className="pdf-icon-link"
                  title="Download PDF"
                >
                  <FaFilePdf className="icon-large" style={{ color: "#d32f2f" }} />
                  <span> View PDF</span>
                </a>
              )}

              {selectedArticle.keywords && (
                <div className="article-keywords">
                  <strong>Keywords:</strong>{" "}
                  {(Array.isArray(selectedArticle.keywords)
                    ? selectedArticle.keywords
                    : selectedArticle.keywords.split(",")
                  )
                    .map((kw) => kw.trim())
                    .filter(Boolean)
                    .map((kw, i) => (
                      <button
                        key={i}
                        className="keywords-tag"
                        onClick={() => handleKeywordClick(kw)}
                      >
                        {kw}
                      </button>
                    ))}
                </div>
              )}

              <div className="article-abstract">
                <h3 className="section-heading">Abstract</h3>
                <p>{selectedArticle.abstract || "No abstract available."}</p>
              </div>

              <div className="button-wrapper">
                <button
                className="summarize-button" 
                onClick={handleSummarize}>Summarize</button>
                {onOpenChat && (
                  <button className="chat-button" onClick={onOpenChat}>
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
        <div className="summary-article-card full-width">
          <button className="close-summary" onClick={() => setShowSummary(false)}>
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
