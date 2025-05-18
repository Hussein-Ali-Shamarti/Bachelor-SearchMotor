import React, { useState, useEffect } from "react";
import axios from "axios";

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
             

  <h1 className="article-title">
  {selectedArticle.title}
</h1>
             

<div className="article-authors">
  <strong>Authors:</strong>
  <div className="authors-list">
    {authorList.map((author, index) => (
      <button
        key={index}
        className="keywords-tag"
        onClick={() => handleKeywordClick(author)}
      >
        {author}
      </button>
    ))}
  </div>
</div>

  <div className="article-meta-block">
     {selectedArticle.conference_name && (
                  <div className="article-conference">
                    Conference: {selectedArticle.conference_name}
                  </div>
                )}
    <div className="article-location">Conference Location: {selectedArticle.conference_location}</div>
    <div className="article-date">Publication Date: {selectedArticle.publication_date}</div>
    <div className="article-isbn">ISBN: {selectedArticle.isbn}</div>
     </div>
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

    <hr className="section-divider" />
   
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
