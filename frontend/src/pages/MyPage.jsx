import React from "react";
import { useLocation } from "react-router-dom";
import SearchHistory from "../components/SearchHistory";
import Header from "../components/Header";
import Search from "../components/Search";

const MyPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const searchQuery = queryParams.get("query");

  return (
    <div className="default-container">
      <Header />
      <SearchHistory />
      <Search initialQuery={searchQuery} />
    </div>
  );
};

export default MyPage;