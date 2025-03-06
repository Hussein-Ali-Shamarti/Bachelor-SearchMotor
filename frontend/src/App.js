import React from "react";

import "./assets/styles/global/basis.css";
import "./assets/styles/global/content.css";
import "./assets/styles/global/feedback.css";
import "./assets/styles/global/header.css";
import "./assets/styles/global/layout.css";
import "./assets/styles/global/layout-modern.css";
import "./assets/styles/global/navi-responsive.css";
import "./assets/styles/global/smart-search.css";

import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import HomePage from "./pages/HomePage";
import MyPage from "./pages/MyPage";

const Home = () => <h1>Welcome to the Home Page</h1>;

function App() {
  return (
    <Router>
      <nav style={{ padding: "10px", borderBottom: "1px solid #ddd" }}>
        <Link to="/" style={{ marginRight: "10px" }}>
          Home
        </Link>
        <Link to="/search" style={{ marginRight: "10px" }}>Search</Link>
        <Link to="/mypage">My Page</Link>
      </nav>
      <Routes>
      <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/mypage" element={<MyPage />} />
      </Routes>
    </Router>
  );
}

export default App;
