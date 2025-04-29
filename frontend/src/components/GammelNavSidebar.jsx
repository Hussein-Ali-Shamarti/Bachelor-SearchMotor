import React, { useState } from "react";
import {
  FiChevronLeft,
  FiChevronRight,
  FiSearch,
  FiMessageSquare
} from "react-icons/fi"; // 🧠 Bare Feather Icons
import "../assets/styles/NavSidebar.css";

const NavSidebar = () => {
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <aside className={`nav-sidebar ${isOpen ? "open" : "collapsed"}`}>
      <div className="nav-header">
        <button onClick={toggleSidebar} className="nav-button">
          {isOpen ? <FiChevronLeft size={24} /> : <FiChevronRight size={24} />}
        </button>

        {isOpen && (
          <>
            <button onClick={() => alert("You must be logged in to search history.")} className="nav-button">
              <FiSearch size={24} />
            </button>
            <button onClick={() => alert("Start a new chat")} className="nav-button">
              <FiMessageSquare size={24} />
            </button>
          </>
        )}
      </div>
    </aside>
  );
};

export default NavSidebar;
