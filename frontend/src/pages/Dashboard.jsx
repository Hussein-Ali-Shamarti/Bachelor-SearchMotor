import React, { useState } from "react";

import HeaderDashboard from "../components/HeaderDashboard";
import SearchInput from "../components/SearchInput";
import SidebarMain from "../components/SidebarMain";
import ArticleSection from "../components/ArticleSection";

import "../assets/styles/Dashboard.css";

const Dashboard = () => {
  const [isSidebarHidden, setIsSidebarHidden] = useState(true);

  const toggleSidebar = () => {
    setIsSidebarHidden(!isSidebarHidden);
  };

  return (
    <div className={`dashboard-layout ${isSidebarHidden ? "no-nav" : ""}`}>

      {/* SIDEBAR VENSTRE */}
      <aside className={`nav-sidebar ${isSidebarHidden ? "hidden" : "active"}`}>
        <SidebarMain toggleSidebar={toggleSidebar} />
      </aside>

      {/* HOVEDKOLONNE */}
      <main className="main-column">
        <HeaderDashboard
          toggleSidebar={toggleSidebar}
          isSidebarHidden={isSidebarHidden}
        />
        <section className="search-input">
          <SearchInput />
        </section>
        <ArticleSection />
      </main>

    </div>
  );
};

export default Dashboard;
