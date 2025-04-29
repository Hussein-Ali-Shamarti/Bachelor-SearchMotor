import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiArrowLeftCircle, FiArrowRightCircle, FiSearch, FiMessageCircle } from "react-icons/fi";

import "../assets/styles/global/header.css";
import "../assets/styles/HeaderMyDashboard.css";

const HeaderMyDashboard = () => {
  const navigate = useNavigate();
  const [navSidebarHidden, setNavSidebarHidden] = useState(false);
  const [aiSidebarHidden, setAiSidebarHidden] = useState(false);

  const toggleNavSidebar = () => {
    const navSidebar = document.querySelector('.nav-sidebar');
    if (navSidebar) {
      navSidebar.classList.toggle('hidden');
      setNavSidebarHidden(!navSidebarHidden);
    }
  };

  const toggleAiSidebar = () => {
    const aiSidebar = document.querySelector('.ai-sidebar');
    if (aiSidebar) {
      aiSidebar.classList.toggle('hidden');
      setAiSidebarHidden(!aiSidebarHidden);
    }
  };

  return (
    <header className="site-header">
      {/* Pil alene */}
      <div className="sidebar-back-button">
        <button
          className="sidebar-hide-toggle"
          onClick={toggleNavSidebar}
          style={{
            transform: navSidebarHidden ? "rotate(180deg)" : "rotate(0deg)",
            transition: "transform 0.3s ease"
          }}
        >
          <FiArrowLeftCircle />
        </button>
      </div>

      {/* Lupe + Chat + Logo samlet */}
      <div className="sidebar-main-controls">
        {/* Gruppe som forsvinner når sidebar skjules */}
        <div
          className="sidebar-icons"
          style={{
            display: navSidebarHidden ? "none" : "flex",
            gap: "0.8rem",
            alignItems: "center"
          }}
        >
          <button className="sidebar-search-toggle">
            <FiSearch />
          </button>
          <button className="sidebar-chat-toggle">
            <FiMessageCircle />
          </button>
        </div>

        {/* Logo som alltid vises */}
        <div className="logo-container">
          <a href="/">
            <img
              src="/images/logo.HybridSearch.svg"
              srcSet="/images/logo.HybridSearch.svg 2x"
              alt="HybridSearch.ai Logo"
              width="222"
              height="36"
            />
          </a>
          <h1>HybridSearch.ai</h1>
        </div>
      </div>

      {/* AI Sidebar-switcher på høyre side */}
      <div className="sidebar-switcher-ai" style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
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
            cursor: "pointer"
          }}
        >
          <FiArrowRightCircle />
        </button>
      </div>
    </header>
  );
};

export default HeaderMyDashboard;
