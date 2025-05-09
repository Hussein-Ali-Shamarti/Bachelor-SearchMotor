// Løsning i JSX for å sikre at både article-sidebar og ai-sidebar alltid vises på desktop og ved navigasjon

import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FiMessageCircle, FiList, FiSearch, FiCpu } from "react-icons/fi";
import "../assets/styles/ArticleSection.css";

function ArticleSection() {
  // Tilstander for å kontrollere visning av sidebars og visningen i article-sidebar
  const [sidebarHidden, setSidebarHidden] = useState(false);
  const [aiSidebarHidden, setAiSidebarHidden] = useState(false);
  const [sidebarView, setSidebarView] = useState("articles");
  const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 1024);

  // Henter nåværende URL for å detektere navigasjon
  const location = useLocation();

  // Lytter etter endringer i skjermstørrelse og oppdaterer tilstanden for desktop
  useEffect(() => {
    const handleResize = () => {
      const isNowDesktop = window.innerWidth >= 1024;
      setIsDesktop(isNowDesktop);

      // Når vi er i desktop-visning skal begge sidebars alltid vises
      if (isNowDesktop) {
        setSidebarHidden(false);
        setAiSidebarHidden(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Viser sidebars ved navigasjon til denne siden (f.eks. via søk)
  useEffect(() => {
    setSidebarHidden(false);
    setAiSidebarHidden(false);
  }, [location]);

  // Veksler synligheten til article-sidebar på mobil og tablet
  const toggleSidebar = () => {
    if (!isDesktop) {
      setSidebarHidden(!sidebarHidden);
    }
  };

  // Veksler synligheten til ai-sidebar på mobil og tablet
  const toggleAiSidebar = () => {
    if (!isDesktop) {
      setAiSidebarHidden(!aiSidebarHidden);
    }
  };

  // Bytter visning i article-sidebar (mellom artikler og chat)
  const openSidebarWithView = (view) => {
    setSidebarView(view);
    if (sidebarHidden && !isDesktop) setSidebarHidden(false);
  };

  return (
    <section className="article-section">
      {/* ARTICLE SIDEBAR - vises alltid på desktop, og kan toggles på mobil og tablet */}
      {(!sidebarHidden || isDesktop) && (
        <div className="article-sidebar">
          {/* Lukkeknapp vises kun på mobil og tablet */}
          {!isDesktop && (
            <button onClick={toggleSidebar} className="close-article-sidebar-mobile">
              Close ✖
            </button>
          )}

          {/* Viser liste over artikler */}
          {sidebarView === "articles" && (
            <ul className="results-list">
              <li className="result-item">
                <h4>Article Title 1</h4>
                <p><strong>Author:</strong> Alice</p>
              </li>
              <li className="result-item">
                <h4>Article Title 2</h4>
                <p><strong>Author:</strong> Bob</p>
              </li>
            </ul>
          )}

          {/* Viser chat-innhold i sidebaren */}
          {sidebarView === "chat" && (
            <div className="chat-container">
              <h3>Chat about this article</h3>
              <p>This is where the AI chat will appear.</p>
            </div>
          )}
        </div>
      )}

      {/* AI SIDEBAR - vises alltid på desktop, og kan toggles på mobil og tablet */}
      {(!aiSidebarHidden || isDesktop) && (
        <div className="ai-sidebar">
          {!isDesktop && (
            <button onClick={toggleAiSidebar} className="close-article-sidebar-mobile">
              Close ✖
            </button>
          )}
          <div className="chat-container">
            <h3>AI Assistant</h3>
            <p>This is where AI-related content appears.</p>
          </div>
        </div>
      )}

      {/* HOVEDINNHOLD - midtseksjonen */}
      <div className="article-content">
        {/* Toppmeny med knapper for å kontrollere sidebars og visning */}
        <div className="article-topbar">
          <button onClick={() => openSidebarWithView("articles")}> 
            <FiList /> Articles
          </button>
          <button onClick={() => openSidebarWithView("chat")}> 
            <FiMessageCircle /> Ask AI
          </button>
          <button>
            <FiSearch /> Article summary
          </button>
          {/* Kun synlig på mobil og tablet for å styre AI-sidebar */}
          {!isDesktop && (
            <button onClick={toggleAiSidebar}> 
              <FiCpu /> Toggle AI Sidebar
            </button>
          )}
        </div>

        {/* Innhold i hovedområdet */}
        <div className="article-body">
          <h3>Selected Article</h3>
          <p><strong>Title:</strong> Example Title</p>
          <p><strong>Author(s):</strong> Example Author</p>
          <p><strong>Abstract:</strong> Full abstract text here...</p>
        </div>
      </div>
    </section>
  );
}

export default ArticleSection;
