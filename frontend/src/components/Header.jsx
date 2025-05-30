// Denne komponenten viser toppteksten (header) på siden, inkludert logo og tittel.
// Den benytter React Router for navigasjon og CSS for stilsetting.


import React from "react";
import { useNavigate } from "react-router-dom";
import "../assets/styles/global/header.css";

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className="site-header">
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
    </header>
  );
};

export default Header;
