import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import SearchPage from "./SearchPage";
import MyPage from "./pages/MyPageF/MyPage";
import HomePage from "./pages/HomePage";



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
