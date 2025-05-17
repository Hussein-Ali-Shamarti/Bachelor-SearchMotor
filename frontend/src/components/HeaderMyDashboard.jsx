import React, { forwardRef, useState } from "react";

import "../assets/styles/global/header.css";
import "../assets/styles/HeaderMyDashboard.css";
import { FiArrowLeftCircle, FiMessageCircle, FiSearch } from "react-icons/fi";

const HeaderMyDashboard = forwardRef(({
  articleSidebarHidden,
  aiSidebarHidden,
  toggleArticleSidebar,
  toggleAiSidebar,
  onSearch,
  clearSelectedArticle,
  queryText,
  setQueryText
}, ref) => {
  const query = queryText;

const handleSearch = () => {
  if (onSearch && query.trim()) {
    if (clearSelectedArticle) clearSelectedArticle();

    const currentSearch = new URLSearchParams(window.location.search).get("query");
    if (currentSearch !== query.trim()) {
      onSearch(query.trim());
    }
  }
};

  return (
    <div className="header-fixed-top" ref={ref}>
      <header className="site-header">
        <div className="inside">
          <div className="MyHeader-content">
            <div className="logo-container">
              <a href="/">
                <img
                  src="/images/logo.HybridSearch.svg"
                  srcSet="/images/logo.HybridSearch.svg 2x"
                  alt="Logo"
                  className="site-logo"
                />
              </a>
              <h1 className="site-title">HybridSearch.ai</h1>
            </div>
            <div className="search-bar-wrapper">
              <input
                type="text"
                placeholder="Search for articles..."
                className="search-input"
                value={query}
                onChange={(e) => setQueryText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleSearch();
                  }
                }}
              />
              <FiSearch
                className="search-icon"
                aria-label="Search"
                onClick={handleSearch}
                style={{ cursor: "pointer" }}
              />
            </div>
          </div>
        </div>
      </header>

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
          <span style={{ fontSize: "1rem", fontWeight: "500" }}>AI Assistant</span>
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
    </div>
  );
});

export default HeaderMyDashboard;
