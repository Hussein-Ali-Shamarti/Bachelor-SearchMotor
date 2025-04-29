import React from "react";
import { FiSearch, FiEdit } from "react-icons/fi";
import "../assets/styles/SidebarMain.css";

function SidebarMain({ toggleSidebar }) {
  return (
    <div className="sidebar-main-content">
      {/* Lukkeknapp for mobil */}
      <button onClick={toggleSidebar} className="close-button-mobile">
  Lukk ✖
</button>

      {/* Øverste ikoner */}
      <ul className="sidebar-icons">
        <li><FiSearch /></li>
        <li><FiEdit /></li>
      </ul>

      <div className="sidebar-content">
        <ul>

        <li>search history</li>
        <li>search history</li>
        <li>search history</li>
        <li>search history</li>
        <li>search history</li>
        <br />
        <br />
        <li>login osv</li>
        <li>skal i footer</li>
          </ul>
        
        </div>

      {/* Footer nederst */}
      <div className="sidebar-footer">
        <button className="auth-button">Login</button>
        <button className="auth-button">Register</button>
      </div>
    </div>
  );
}

export default SidebarMain;
