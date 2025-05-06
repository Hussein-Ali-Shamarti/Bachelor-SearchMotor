import React, { useState, useEffect, useRef } from "react";

import "../assets/styles/MyDashboard.css";
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
  const [visibleCount, setVisibleCount] = useState(5);


  const sidebarRef = useRef(null); // ✔️ beholdt – brukes til scroll
  const [showLoadMore, setShowLoadMore] = useState(false); // ✔️ beholdt – styrer "Last flere"-knapp

  const handleSidebarScroll = () => {
    const el = sidebarRef.current;
    if (!el) return;

    if (el.scrollTop + el.clientHeight >= el.scrollHeight - 10) {
      setShowLoadMore(true);
    } else {
      setShowLoadMore(false);
    }
  };

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const mobile = width <= 600;
      const tablet = width > 600 && width <= 1024;
      setIsMobile(mobile);
      setIsTablet(tablet);

      if (!mobile && !tablet) {
        setArticleSidebarHidden(false);
        setAiSidebarHidden(false);
      } else {
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
      setAiSidebarHidden(true);
    } else {
      setArticleSidebarHidden((prev) => !prev);
    }
  };

  const toggleAiSidebar = () => {
    if (isMobile) {
      setAiSidebarHidden((prev) => !prev);
      setArticleSidebarHidden(true);
    } else {
      setAiSidebarHidden((prev) => !prev);
    }
  };

  const handleSummarize = () => {
    setShowSummary(true);
  };

  return (
    <div className="outer-wrap">
      {/* ✅ Endret: fjernet <div ref={headerRef}> fordi vi ikke måler høyde lenger */}
      <HeaderMyDashboard
        articleSidebarHidden={articleSidebarHidden}
        aiSidebarHidden={aiSidebarHidden}
        toggleArticleSidebar={toggleArticleSidebar}
        toggleAiSidebar={toggleAiSidebar}
      />

      
      
      <div
        className={`dashboard
          ${!articleSidebarHidden && !aiSidebarHidden ? "three-columns" : ""}
          ${articleSidebarHidden && !aiSidebarHidden ? "no-article" : ""}
          ${!articleSidebarHidden && aiSidebarHidden ? "no-ai" : ""}
          ${articleSidebarHidden && aiSidebarHidden ? "only-main" : ""}
        `}
      >
       <aside
  className={`article-sidebar${articleSidebarHidden ? " is-hidden" : ""}`}
  ref={sidebarRef}
  onScroll={handleSidebarScroll}
>

          <div className="nav-squish-container">
  <h3>Article list</h3>
  <nav className="article-list-menu">
    <ul>
      {Array.from({ length: visibleCount }).map((_, i) => (
        <li key={i}>
          <a href="#">
            <div className="article-text">
              <div className="article-title">Measuring the Impact of eGovernment Services</div>
              <div className="article-author">Berntzen, Lasse</div>
            </div>
          </a>
        </li>
      ))}
    </ul>

    {visibleCount < 12 && (
      <div className="article-sidebar-loadmore">
        <button onClick={() => setVisibleCount(prev => prev + 5)}>Last flere</button>
      </div>
    )}
  </nav>
</div>

        </aside>

        <main
  className={`main-area${
    isMobile && (articleSidebarHidden === false || aiSidebarHidden === false)
      ? " is-hidden"
      : ""
  }`}
>
          <section className="dashboard-cards">
            <div className={`selected-article-card ${showSummary ? "half-width" : "full-width"}`}>
              <div className="card-content">
                <h2>Selected Article</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>
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
                  <p>Fusce pulvinar, arcu id venenatis lacinia, nulla risus mattis ligula, vel blandit ipsum nunc in lorem. Sed commodo ligula ut velit consequat, nec fermentum augue fringilla. Aenean non quam vitae nisl tempus faucibus. Curabitur ut sapien ac risus suscipit sagittis. Nullam a ligula et magna tincidunt imperdiet. Cras posuere, sapien at varius blandit, metus augue sollicitudin enim, nec euismod nibh justo a metus.</p>

                </div>
              </div>
            )}
          </section>
        </main>

        <aside
 
 className={`ai-sidebar${aiSidebarHidden ? " is-hidden" : ""}${isTablet && !aiSidebarHidden ? " overlay" : ""}`}

>

  

        
          <div className="ai-squish-container">
            <h3>AI Tools:</h3>
            <input type="text" placeholder="Search in AI Assistant..." className="ai-input" />
            <p>AI assistant content placeholder...</p>
          </div>
        </aside>
      </div>
      <footer className="site-footer">
  <div className="inside">
    <div className="footer-text">
      HybridSearch.ai – Bachelorprosjekt
    </div>
  </div>
</footer>
    </div>
  );
}

export default MyDashboard;
