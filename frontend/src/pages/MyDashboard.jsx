import React, { useState, useEffect } from "react";
import "../assets/styles/MyDashboard.css";
import {
  FiList,
  FiFileText,
  FiMessageCircle,
  FiArrowLeftCircle,
} from "react-icons/fi";
import HeaderMyDashboard from "../components/HeaderMyDashboard";

function MyDashboard() {
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [showSummary, setShowSummary] = useState(false);
  const [articleSidebarHidden, setArticleSidebarHidden] = useState(true);
  const [aiSidebarHidden, setAiSidebarHidden] = useState(true);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 600);
  const [isTablet, setIsTablet] = useState(
    window.innerWidth > 600 && window.innerWidth <= 1024
  );

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const mobile = width <= 600;
      const tablet = width > 600 && width <= 1024;

      setIsMobile(mobile);
      setIsTablet(tablet);

      if (!mobile && !tablet) {
        // Desktop: vis alt
        setArticleSidebarHidden(false);
        setAiSidebarHidden(false);
      } else {
        // Mobil og nettbrett: start med alt skjult
        setArticleSidebarHidden(true);
        setAiSidebarHidden(true);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  const toggleArticleSidebar = () => {
    if (isMobile) {
      setArticleSidebarHidden((prev) => !prev);
      setAiSidebarHidden(true); // På mobil: fortsatt én åpen om gangen
    } else {
      setArticleSidebarHidden((prev) => !prev);
    }
  };
  
  const toggleAiSidebar = () => {
    if (isMobile) {
      setAiSidebarHidden((prev) => !prev);
      setArticleSidebarHidden(true); // På mobil: fortsatt én åpen om gangen
    } else {
      setAiSidebarHidden((prev) => !prev);
    }
  };
  

  const handleSummarize = () => {
    setShowSummary(true);
  };

  return (
    <div className="outer-wrap">
      <HeaderMyDashboard />

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
              fontSize: "1.4rem",
              background: "none",
              border: "none",
              color: "inherit",
              cursor: "pointer",
            }}
          >
            <FiMessageCircle />
          </button>
        </div>
      </div>

      <div className="dashboard">
        <aside className={`article-sidebar ${articleSidebarHidden ? "hidden" : ""}`}>
          <div className="nav-squish-container">
            <h3>Article list</h3>
            <nav className="article-list-menu">
            <ul>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
      
    </a>
  </li>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
    
    </a>
  </li>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
     
    </a>
  </li>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
      
    </a>
  </li>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
      
    </a>
  </li>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
      
    </a>
  </li>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
      
    </a>
  </li>
  <li>
    <a href="#">
      <h3>Measuring the Impact of eGovernment Services</h3>
      <p><strong>Author(s):</strong> ['Berntzen, Lasse']</p>
      
    </a>
  </li>
</ul>

            </nav>
          </div>
        </aside>

        <main className={`main-area ${(isMobile && (!articleSidebarHidden || !aiSidebarHidden)) ? 'hidden' : ''}`}>
          <section className="dashboard-cards">
            <div className={`selected-article-card ${showSummary ? "half-width" : "full-width"}`}>
              <div className="card-content">
                <h2>Selected Article</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer metus mi, porttitor id mollis auctor.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer metus mi, porttitor id mollis auctor.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer metus mi, porttitor id mollis auctor.</p>
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
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.</p>


                </div>
              </div>
            )}
          </section>

        
        </main>
{/* ai-sidebar for en overlay klasse for tablet view */}

<aside
  className={`ai-sidebar ${aiSidebarHidden ? "hidden" : ""} ${isTablet && !aiSidebarHidden ? "overlay" : ""}`}
>
  <button
    className="close-ai-button"
    onClick={() => setAiSidebarHidden(true)}
  >
    &times;
  </button>

  <div className="ai-squish-container">
    <h3>AI Tools:</h3>
    

    <input
      type="text"
      placeholder="Search in AI Assistant..."
      className="ai-input"
    />
    <p>Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi elit posuere nunc, id blandit tellus quam vel augue.Fusce pulvinar, arcu id venenatis lacinia, nisi</p>
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
