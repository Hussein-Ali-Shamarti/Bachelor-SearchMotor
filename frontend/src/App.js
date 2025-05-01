import React from "react";

import "./assets/styles/global/basis.css";
import "./assets/styles/global/content.css";
import "./assets/styles/global/feedback.css";
import "./assets/styles/global/header.css";
import "./assets/styles/global/layout.css";
import "./assets/styles/global/layout-modern.css";
import "./assets/styles/global/navi-responsive.css";
import "./assets/styles/global/smart-search.css";
import "./assets/styles/global/menu.css";

import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import HomePage from "./pages/HomePage";
import MyPage from "./pages/MyPage";
import Login from "./pages/Login";
import Registration from "./pages/Registration";

import MyDashboard from "./pages/MyDashboard"; // Ny MyDashboard second 

function App() {
  return (
    <Router>
      <nav className="main-nav" style={{ padding: "10px", borderBottom: "1px solid #ddd" }}>
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/search" className="nav-link">Search</Link>
        <Link to="/mypage" className="nav-link">My Page</Link>
        <Link to="/login" className="nav-link">Login</Link>
        <Link to="/register" className="nav-link">Register</Link>
    
        <Link to="/mydashboard" className="nav-link">MyDashboard</Link> {/* Riktig path */}
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/mypage" element={<MyPage />} />
      
        <Route path="/mydashboard" element={<MyDashboard />} /> {/* Ny rute */}

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Registration />} />
      </Routes>
    </Router>
  );
}

export default App;
