import React, { useState } from "react";
import "../assets/styles/MyDashboard.css";
import {
  FiList,
  FiFileText,
  FiMessageCircle,
  FiArrowLeftCircle,
  FiArrowRightCircle,
} from "react-icons/fi";
import HeaderMyDashboard from "../components/HeaderMyDashboard";

function MyDashboard() {
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [showSummary, setShowSummary] = useState(false);
  const [articleSidebarHidden, setArticleSidebarHidden] = useState(false);
  const [aiSidebarHidden, setAiSidebarHidden] = useState(false);

  const toggleArticleSidebar = () => {
    setArticleSidebarHidden((prev) => !prev);
  };

  const toggleAiSidebar = () => {
    setAiSidebarHidden((prev) => !prev);
  };

  const handleSummarize = () => {
    setShowSummary(true);
  };

  return (
    <div className="outer-wrap">
      <HeaderMyDashboard />

      {/* Kontrollpanel for navigasjon mellom sidebars */}
      <div className="control-panel-nav">
        <div className="sidebar-switcher-article">
          <button
            className="sidebar-hide-toggle"
            onClick={toggleArticleSidebar}
            style={{
              transform: articleSidebarHidden ? "rotate(180deg)" : "rotate(0deg)",
              transition: "transform 0.3s ease",
              fontSize: "1.4rem",
              background: "none",
              border: "none",
              color: "inherit",
              cursor: "pointer",
            }}
          >
            <FiArrowLeftCircle />
          </button>
          <span style={{ fontSize: "1rem", fontWeight: "500" }}>Article List</span>
        </div>

        <div className="sidebar-switcher-ai">
          <span style={{ fontSize: "1rem", fontWeight: "500" }}>AI Assistent</span>
          <button
            className="sidebar-ai-toggle"
            onClick={toggleAiSidebar}
            style={{
              transform: aiSidebarHidden ? "rotate(180deg)" : "rotate(0deg)",
              transition: "transform 0.3s ease",
              fontSize: "1.4rem",
              background: "none",
              border: "none",
              color: "inherit",
              cursor: "pointer",
            }}
          >
            <FiArrowRightCircle />
          </button>
        </div>
      </div>

      <div className="dashboard">
        {!articleSidebarHidden && (
          <aside className="article-sidebar">
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
        )}

        <main className={`main-area ${articleSidebarHidden ? "expand" : ""}`}>
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
                  <a href="#" onClick={toggleAiSidebar}>
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

        {!aiSidebarHidden && (
          <aside className="ai-sidebar">
            <div className="ai-squish-container">
              <h3>AI Tools:</h3>
              <p>Chat or summary output comes here...</p>
            </div>
          </aside>
        )}
      </div>

      <footer className="footer-area">
        <p>HybridSearch.ai – Bachelorprosjekt</p>
      </footer>
    </div>
  );
}

export default MyDashboard;

