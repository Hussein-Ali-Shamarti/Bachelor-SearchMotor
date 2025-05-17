import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

function ArticleList({ searchQuery, isMobile, isTablet, onSelectArticle }) {
  const [articles, setArticles] = useState([]);
  const [visibleCount, setVisibleCount] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const sidebarRef = useRef(null);

  const lastQueryRef = useRef(null);

useEffect(() => {
  if (!searchQuery || searchQuery === lastQueryRef.current) return;
  lastQueryRef.current = searchQuery;

  const fetchArticles = async () => {
    setLoading(true);
    setError(null);

    try {
      const embeddingResponse = await axios.post(
        "http://127.0.0.1:5001/generate-embedding",
        { text: searchQuery }
      );

      const embedding = embeddingResponse.data.embedding;

      const searchResponse = await axios.post(
        "http://127.0.0.1:5001/ai-search",
        {
          query: searchQuery,
          embedding: embedding,
          k: 50,
        }
      );

      if (Array.isArray(searchResponse.data) && searchResponse.data.length > 0) {
        setArticles(searchResponse.data);
      } else {
        setArticles([]);
        setError("No articles found.");
      }
    } catch (err) {
      console.error(err);
      setArticles([]);

      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError("Failed to fetch articles.");
      }
    } finally {
      setLoading(false);
    }
  };

  fetchArticles();
}, [searchQuery]);


  const handleSidebarScroll = () => {
    const el = sidebarRef.current;
    if (!el) return;

    if (el.scrollTop + el.clientHeight >= el.scrollHeight - 10) {
      setVisibleCount((prev) => prev + 5);
    }
  };

  return (
    <aside
      className="article-sidebar"
      ref={sidebarRef}
      onScroll={handleSidebarScroll}
    >
      <div className="nav-squish-container">
        <nav className="article-list-menu">
          {loading && <p>Loading articles...</p>}
          {error && <p className="error">{error}</p>}
          {!loading && !error && searchQuery && (
            <div className="query-summary">
              <em>Showing results for:</em> {searchQuery}
            </div>
          )}
          <ul>
            {articles.slice(0, visibleCount).map((article) => (
              <li key={article.id}>
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    onSelectArticle(article);
                  }}
                >
                  <div className="article-text">
                    <div className="article-title">
                      {article.title || "No Title"}
                    </div>
                    <div className="article-author">
                      {(article.author || "Unknown Author").trim()}
                      {article.publication_date && (
                        <span> - {article.publication_date}</span>
                      )}
                    </div>
                  </div>
                </a>
              </li>
            ))}
          </ul>

          {articles.length > visibleCount && (
            <div className="article-sidebar-loadmore">
              <button onClick={() => setVisibleCount((prev) => prev + 5)}>
                Load more results
              </button>
            </div>
          )}
        </nav>
      </div>
    </aside>
  );
}

export default ArticleList;
