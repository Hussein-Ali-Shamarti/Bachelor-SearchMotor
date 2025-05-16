import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
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
  const [userOpenedChat, setUserOpenedChat] = useState(false);

  const navigate = useNavigate();
  // Clears selected article
  const clearArticle = () => setSelectedArticle(null);
  const [queryText, setQueryText] = useState("");

  // Handles search query (used by header + ArticleDetails)
  const handleSearch = (query) => {
    clearArticle();
    navigate(`?query=${encodeURIComponent(query)}`);
    console.log("Dashboard: new search triggered with query:", query);
  };


  // Handle resizing
  useEffect(() => {
  const handleResize = () => {
    const width = window.innerWidth;
    const mobile = width <= 600;
    const tablet = width > 600 && width <= 1024;
    setIsMobile(mobile);
    setIsTablet(tablet);
    // On desktop, DO NOTHING — keep current sidebar state
  };

  window.addEventListener("resize", handleResize);
  return () => window.removeEventListener("resize", handleResize);
}, []);

useEffect(() => {
  const width = window.innerWidth;
  const isDesktop = width > 1024;

  if (isDesktop && !userOpenedChat) {
    setAiSidebarHidden(true); // Force hide unless user clicked Chat
  }
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
      clearSelectedArticle={clearArticle}
      queryText={queryText}                             
      setQueryText={setQueryText}                       
      onSearch={(query) => {
        clearArticle();
        setQueryText(query);                            
        navigate(`?query=${encodeURIComponent(query)}`);
        console.log("Dashboard: new search triggered with query:", query);
      }}
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
            setUserOpenedChat(true);
            if (isMobile) {
              setAiSidebarHidden(false);
              setArticleSidebarHidden(true);
            } else {
              setAiSidebarHidden(false);
            }
          }}
          onSearch={handleSearch}
          clearSelectedArticle={clearArticle} 
          setQueryText={setQueryText}
          />
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
