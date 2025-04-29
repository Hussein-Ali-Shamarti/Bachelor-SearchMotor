import React from "react";
import "../assets/styles/Dashboard.css"; // Styling ligger fortsatt her

// Importer ikonene (husk at du må ha riktige paths)
import searchIcon from "../assets/images/search.svg"; 
import nyChatIcon from "../assets/images/Nychat.svg"; 

function SidebarMain() {
  return (
    <aside className="nav-sidebar">

      {/* Handling-knapper med ikoner */}
      <div className="sidebar-actions">
        <button className="icon-button" onClick={() => alert('New Search clicked!')}>
          <img src={searchIcon} alt="Search Icon" width="25px" height="25px" />
        </button>
        <button className="icon-button" onClick={() => alert('Search History clicked!')}>
          <img src={nyChatIcon} alt="Chat Icon" width="25px" height="25px" />
        </button>
      </div>

      {/* Meny under */}
      <div className="sidebar-top">
        <h3>Explore:</h3>
        <nav className="example-menu">
          <ul>
            <li><a href="#">Search History 1</a></li>
            <li><a href="#">Search History 2</a></li>
            <li><a href="#">Search History 3</a></li>
          </ul>
        </nav>
      </div>

      {/* Footer med login/registration */}
      <div className="sidebar-footer">
        <button className="auth-button">Login</button>
        <button className="auth-button">Register</button>
      </div>

    </aside>
  );
}

export default SidebarMain;
