import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import SearchWithResults from "../components/SearchWithResults";
import Sidebar from "../components/Sidebar";
import user from "../assets/images/user.svg";
import question from "../assets/images/question.svg";
import   "../assets/styles/MyPage.css";
import Popup from "../components/Popup";

const MyPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const [searchQuery, setSearchQuery] = useState(queryParams.get("query") || "");


  //TODO: we should probably base this list on a list from the server instead of local changes
  // Initialize searchHistory from sessionStorage or as an empty array, store to sessionStorage
  const [searchHistory, setSearchHistory] = useState(() => {
    const savedHistory = sessionStorage.getItem("searchHistory");
    return savedHistory ? JSON.parse(savedHistory) : [];
  });

  // Update sessionStorage whenever searchHistory changes
  useEffect(() => {
    sessionStorage.setItem("searchHistory", JSON.stringify(searchHistory));
  }, [searchHistory]);

  // Function given to SearchWithResults-component to add a search-query to searchHistory
  const addToSearchHistory = (query) => {
    const timestamp = new Date().toISOString().split('T')[0];
    setSearchHistory((prevSearchHistory) => [...prevSearchHistory, { searchQuery: query, timestamp: timestamp }]);
  }

  const handleSelectSearchQuery = (query) => {
    setSearchQuery(query);
  }

  return (
    <div className="mypage">
      <Header />
      <Sidebar sidebarVisible="true" searchHistory={searchHistory} handleSelectSearchQuery={handleSelectSearchQuery} />
      <main className="site-content">
        
        <SearchWithResults initialQuery={searchQuery} addToSearchHistory={addToSearchHistory} />
        <button onclick="alert('Person clicked!')" className="user-icon">
            <img src={user} alt="user Icon" width="30px" height="30px"/>
          </button>
          
          <Popup/>
      </main>
    </div>
  );
};

export default MyPage;