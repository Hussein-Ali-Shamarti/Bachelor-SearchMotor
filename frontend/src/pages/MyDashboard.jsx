import React, { useEffect, useState } from "react";
import "../assets/styles/MyDashboard.css";
import { FiList, FiFileText, FiMessageCircle } from "react-icons/fi";
import HeaderMyDashboard from "../components/HeaderMyDashboard";

function MyDashboard() {
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [showSummary, setShowSummary] = useState(false);

  useEffect(() => {
    const leftButton = document.querySelector(".sidebar-left-toggle");
    const rightButton = document.querySelector(".sidebar-right-toggle");

    const toggleLeft = () => {
      document.querySelector(".nav-sidebar").classList.toggle("hidden");
    };

    const toggleRight = () => {
      document.querySelector(".ai-sidebar").classList.toggle("hidden");
    };

    if (leftButton) leftButton.addEventListener("click", toggleLeft);
    if (rightButton) rightButton.addEventListener("click", toggleRight);

    return () => {
      if (leftButton) leftButton.removeEventListener("click", toggleLeft);
      if (rightButton) rightButton.removeEventListener("click", toggleRight);
    };
  }, []);

  const handleSummarize = () => {
    setShowSummary(true);
  };

  return (
    <div className="outer-wrap">
      <HeaderMyDashboard />

      <div className="inside">
        <div className="search-bar-wrapper">
          <input
            type="text"
            placeholder="Search for articles..."
            className="search-input"
          />
        </div>
      </div>

      <div className="dashboard">
        <aside className="nav-sidebar">
          <div className="nav-squish-container">
            <h3>Article list</h3>
            <nav className="example-menu">
              <ul>
                <li><a href="#">article list</a></li>
                <li><a href="#">article list</a></li>
                <li><a href="#">article list</a></li>
                <li><a href="#">article list</a></li>
              </ul>
            </nav>
          </div>
        </aside>

        <main className="main-area">
          <section className="dashboard-cards">
            <div className={`selected-article-card ${showSummary ? "half-width" : "full-width"}`}>
              <div className="card-content">
                <h2>Selected Article</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer metus mi, porttitor id mollis auctor.</p>
                <div className="button-wrapper">
                  <button className="summarize-button" onClick={handleSummarize}>
                    Summarize
                  </button>
                </div>
              </div>
            </div>

            {showSummary && (
  <div className="summary-article-card half-width">
    <button className="close-summary" onClick={() => setShowSummary(false)}>
      &times;
    </button>
    <div className="card-content">
      <h2>AI Summary</h2>
      <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>
    </div>
  </div>
)}
          </section>

          <section className="menu-section">
            <h2 className="menu-heading">AI Navigation</h2>
            <nav id="advanced-nav" className="advanced-nav menu" role="navigation">
              <ul>
                <li>
                  <a href="#">
                    <div className="icon"><FiList /></div>
                    <div className="button-text">
                      Article List
                      <span>View all saved articles</span>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="#" onClick={handleSummarize}>
                    <div className="icon"><FiFileText /></div>
                    <div className="button-text">
                      Summary
                      <span>AI-generated article summary</span>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="#" onClick={() =>
                    document.querySelector(".ai-sidebar").classList.toggle("hidden")
                  }>
                    <div className="icon"><FiMessageCircle /></div>
                    <div className="button-text">
                      Ask AI
                      <span>Chat about your article</span>
                    </div>
                  </a>
                </li>
              </ul>
            </nav>
          </section>
        </main>

        <aside className="ai-sidebar">
          <div className="ai-squish-container">
            <h3>AI Tools:</h3>
            <p>Chat or summary output comes here...</p>
          </div>
        </aside>
      </div>

      <footer className="footer-area">
        <p>HybridSearch.ai – Bachelorprosjekt</p>
      </footer>
    </div>
  );
}

export default MyDashboard;
