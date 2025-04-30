import React, { useState } from "react";
import { FiArrowLeftCircle, FiArrowRightCircle } from "react-icons/fi";

import "../assets/styles/global/header.css";
import "../assets/styles/HeaderMyDashboard.css";

const HeaderMyDashboard = () => {
  const [navSidebarHidden, setNavSidebarHidden] = useState(false);
  const [aiSidebarHidden, setAiSidebarHidden] = useState(false);

  const toggleNavSidebar = () => {
    const navSidebar = document.querySelector(".nav-sidebar");
    if (navSidebar) {
      navSidebar.classList.toggle("hidden");
      setNavSidebarHidden(!navSidebarHidden);
    }
  };

  const toggleAiSidebar = () => {
    const aiSidebar = document.querySelector(".ai-sidebar");
    if (aiSidebar) {
      aiSidebar.classList.toggle("hidden");
      setAiSidebarHidden(!aiSidebarHidden);
    }
  };

  return (
    <header className="site-header">
      {/* VENSTRE: pil + tekst utenfor .inside */}
      <div className="sidebar-back-button">
        <button
          className="sidebar-hide-toggle"
          onClick={toggleNavSidebar}
          style={{
            transform: navSidebarHidden ? "rotate(180deg)" : "rotate(0deg)",
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

      {/* MIDTEN: Logo */}
      <div className="inside">
        <div className="wrapper">
          <div className="logo-container">
            <a href="/">
              <img
                src="/images/logo.HybridSearch.svg"
                srcSet="/images/logo.HybridSearch.svg 2x"
                alt="Logo"
                width="222"
                height="36"
              />
            </a>
            <h1>HybridSearch.ai</h1>
          </div>
        </div>
      </div>

      {/* HØYRE: AI-knapp og tekst utenfor .inside */}
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
    </header>
  );
};

export default HeaderMyDashboard;
