import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "../assets/styles/MyDashboard.css";
import HeaderMyDashboard from "../components/HeaderMyDashboard";
import ArticleList from "../components/ArticleList";
import ArticleDetails from "../components/ArticleDetails";
import ChatSection from "../components/ChatSection";

function MyDashboard() {
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleSidebarHidden, setArticleSidebarHidden] = useState(false);
  const [aiSidebarHidden, setAiSidebarHidden] = useState(true);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 600);
  const [isTablet, setIsTablet] = useState(
    window.innerWidth > 600 && window.innerWidth <= 1024
  );

  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const searchQuery = queryParams.get("query");
  const [chatHistory, setChatHistory] = useState([]);


  // Handle resizing
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const mobile = width <= 600;
      const tablet = width > 600 && width <= 1024;
      setIsMobile(mobile);
      setIsTablet(tablet);

      if (!mobile && !tablet) {
        setArticleSidebarHidden(false);
        setAiSidebarHidden(false);
      } else {
        setArticleSidebarHidden(true);
        setAiSidebarHidden(true);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="outer-wrap">
      <HeaderMyDashboard
        articleSidebarHidden={articleSidebarHidden}
        aiSidebarHidden={aiSidebarHidden}
        toggleArticleSidebar={() =>
          isMobile
            ? (setArticleSidebarHidden((prev) => !prev), setAiSidebarHidden(true))
            : setArticleSidebarHidden((prev) => !prev)
        }
        toggleAiSidebar={() =>
          isMobile
            ? (setAiSidebarHidden((prev) => !prev), setArticleSidebarHidden(true))
            : setAiSidebarHidden((prev) => !prev)
        }
      />

      <div
        className={`dashboard
          ${!articleSidebarHidden && !aiSidebarHidden ? "three-columns" : ""}
          ${articleSidebarHidden && !aiSidebarHidden ? "no-article" : ""}
          ${!articleSidebarHidden && aiSidebarHidden ? "no-ai" : ""}
          ${articleSidebarHidden && aiSidebarHidden ? "only-main" : ""}
          ${chatHistory.length > 0 && !aiSidebarHidden ? "chat-active" : ""}
          ${!selectedArticle ? "no-article-selected" : ""}
        `}
      >
        {!articleSidebarHidden && (
          <ArticleList
            searchQuery={searchQuery}
            isMobile={isMobile}
            isTablet={isTablet}
            onSelectArticle={(article) => {
              setSelectedArticle(article);
              if (isMobile || isTablet) {
                setArticleSidebarHidden(true);
              }
            }}
          />
        )}

        <main
          className={`main-area${
            isMobile &&
            (articleSidebarHidden === false || aiSidebarHidden === false)
              ? " is-hidden"
              : ""
          }`}
        >
          <ArticleDetails 
          selectedArticle={selectedArticle}
          onOpenChat={() => {
            if (isMobile) {
              setAiSidebarHidden(false);
              setArticleSidebarHidden(true);
            } else {
              setAiSidebarHidden(false);
            }
          }} />
        </main>

        {!aiSidebarHidden && (
          <ChatSection 
          selectedArticle={selectedArticle}
          chatHistory={chatHistory}
          setChatHistory={setChatHistory}
          />
        )}
      </div>

      <footer className="site-footer">
        <div className="inside">
          <div className="footer-text">HybridSearch.ai – Bachelorprosjekt</div>
        </div>
      </footer>
    </div>
  );
}

export default MyDashboard;
