import React, { useState } from "react";
import { FiMessageCircle, FiList, FiSearch } from "react-icons/fi";
import "../assets/styles/ArticleSection.css";

function ArticleSection() {
  const [sidebarHidden, setSidebarHidden] = useState(false);
  const [sidebarView, setSidebarView] = useState("articles"); // 'articles' eller 'chat'

  const toggleSidebar = () => {
    setSidebarHidden(!sidebarHidden);
  };

  const openSidebarWithView = (view) => {
    setSidebarView(view);
    if (sidebarHidden) setSidebarHidden(false);
  };

  return (
    <section className="article-section">
      
      {/* SIDEBAR */}
      {!sidebarHidden && (
        <div className="article-sidebar">
          {/* Mobil-lukkeknapp */}
          <button onClick={toggleSidebar} className="close-article-sidebar-mobile">
            Close ✖
          </button>

          {/* Sidebar-innhold */}
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

          {sidebarView === "chat" && (
            <div className="chat-container">
              <h3>Chat about this article</h3>
              <p>This is where the AI chat will appear.</p>
            </div>
          )}
        </div>
      )}

      {/* HOVEDINNHOLD */}
      <div className="article-content">

        {/* TOPP-KNAPPER */}
        <div className="article-topbar">
          <button onClick={() => openSidebarWithView("articles")}>
            <FiList /> Articles
          </button>
          <button onClick={() => openSidebarWithView("chat")}>
            <FiMessageCircle /> Ask AI
          </button>
          <button>
            <FiSearch /> New Search
          </button>
        </div>

        {/* ARTIKKELDETALJER */}
        <div className="article-body">
          <h2>Selected Article</h2>
          <p><strong>Title:</strong> Example Title</p>
          <p><strong>Author(s):</strong> Example Author</p>
          <p><strong>Abstract:</strong> Full abstract text here...</p>
        </div>
      </div>
    </section>
  );
}

export default ArticleSection;
