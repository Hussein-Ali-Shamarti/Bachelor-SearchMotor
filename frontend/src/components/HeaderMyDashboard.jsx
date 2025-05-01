import React from "react";

import "../assets/styles/global/header.css";
import "../assets/styles/HeaderMyDashboard.css";

const HeaderMyDashboard = () => {
  return (
    <header className="site-header">
      <div className="inside">
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

        {/* Søkefelt plassert under logo */}
        <div className="search-bar-wrapper">
          <input
            type="text"
            placeholder="Search for articles..."
            className="search-input"
          />
        </div>
      </div>
    </header>
  );
};

export default HeaderMyDashboard;

