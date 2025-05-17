import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import EnterIcon from "../assets/images/Eenter.svg";

const SearchInput = () => {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (query.trim()) {
      navigate(`/MyDashboard?query=${encodeURIComponent(query.trim())}`);
    }
  };

  // Function to handle pressing Enter key
  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <section className="smart-search">
      <div className="inside">
        <h1>What can I help you with?</h1>
        <div className="search-wrapper">
          <input
            type="text"
            id="search-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search for articles..."
            className="search-input"
          />
          <button type="button" onClick={handleSearch} className="Enter-icon">
          <img src={EnterIcon} alt="Enter Icon" />
          </button>
        </div>
      </div>
    </section>
  );
};

export default SearchInput;
