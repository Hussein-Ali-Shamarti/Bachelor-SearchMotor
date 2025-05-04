import React from "react";
import { useNavigate } from "react-router-dom";
import LeftPil from "../assets/images/LeftPil.svg";
import "../assets/styles/HeaderDashboard.css";

const HeaderDashboard = ({ toggleSidebar, isSidebarHidden }) => {
  return (
    <header className="site-header">

      {/* Flex-container for pil og logo */}
      <div className="header-content">

        {/* PIL i egen boks */}
        <div className="sidebar-toggle-container">
          <button
            onClick={toggleSidebar}
            className={`sidebar-toggle-button ${isSidebarHidden ? "rotated" : ""}`}
          >
            <img src={LeftPil} alt="Toggle Sidebar" width="30" height="30" />
          </button>
        </div>

        {/* LOGO i egen boks */}
        <div className="logo-container">
          <a href="/">
            <img
              src="/images/logo.HybridSearch.svg"
              srcSet="/images/logo.HybridSearch.svg 2x"
              alt="HybridSearch Logo"
              width="222"
              height="36"
            />
          </a>
          <h1>HybridSearch.ai</h1>
        </div>

      </div>

    </header>
  );
};

export default HeaderDashboard;
