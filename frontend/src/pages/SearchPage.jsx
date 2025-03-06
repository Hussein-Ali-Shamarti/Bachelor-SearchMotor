import React, { useState } from "react";
import "../assets/styles/SearchPage.css";
import SearchWithResults from "../components/SearchWithResults";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";

const SearchPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const searchQuery = queryParams.get("query");

  return (
    <div className="search-page-container">
      <Header />
      <h1>AI-Powered Search</h1>
      <SearchWithResults initialQuery={searchQuery} />
    </div>
  );
};

export default SearchPage;
