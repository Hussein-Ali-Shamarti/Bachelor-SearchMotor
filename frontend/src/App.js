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
import HomePage from "./pages/HomePage";
import MyDashboard from "./pages/MyDashboard";

function App() {
  return (
    <Router>
     
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/mydashboard" element={<MyDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
