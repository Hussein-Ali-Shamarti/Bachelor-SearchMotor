import React, { useEffect, useState } from "react";
import "../assets/styles/MyDashboard.css";
import { FiList, FiFileText, FiMessageCircle } from "react-icons/fi";
import HeaderMyDashboard from "../components/HeaderMyDashboard";

function MyDashboard() {
  const [selectedArticle, setSelectedArticle] = useState(null);

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
    console.log("Summarizing article...");
    // implementer faktisk AI-kall her senere
  };

  return (
    <div className="outer-wrap">
      {/* Logo/Header */}
      <HeaderMyDashboard />

      {/* Søkefelt */}
      <div className="search-bar-wrapper">
        <input
          type="text"
          placeholder="Search for articles..."
          className="search-input"
        />
      </div>

      <div className="dashboard">
        {/* Venstre side - artikkelliste */}
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

        {/* Midten - Hovedinnhold */}
        <main className="main-area">
          {/* Valgt artikkel */}
          <section className="selected-article">
            <h2>Selected Article</h2>
            <p>Article details shown here...</p>
          </section>

          {/* Summarize-knapp */}
          <div className="summary-action">
            <button className="summarize-button" onClick={handleSummarize}>
              Summarize
            </button>
          </div>

          {/* AI-navigasjonsknapper */}
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

        {/* Høyre side - AI chat */}
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
