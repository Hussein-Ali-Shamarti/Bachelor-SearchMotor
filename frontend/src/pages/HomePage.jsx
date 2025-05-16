import React from "react";
import SearchInput from "../components/SearchInput";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import "../assets/styles/HomePage.css";

const HomePage = () => {
  const navigate = useNavigate();
  const userisloggedIn = false; // TODO: Update this logic

  const handleSearch = (query) => {
    if (userisloggedIn) {
      navigate(`/mypage?query=${encodeURIComponent(query)}`);
      console.log("Navigating to my page. query=" + query);
    } else {
      navigate(`/MyDashboard?query=${encodeURIComponent(query)}`);
      console.log("Navigating to search page. query=" + query);
    }
  };

  return (
    <div className="home">
      <div className="header-fixed-top">
  <header className="site-header">
    <div className="inside">
      <div className="logo-container">
        <a href="/">
          <img 
            src="/images/logo.HybridSearch.svg" 
            alt="HybridSearch Logo" 
            className="site-logo" 
          />
        </a>
        <h1 className="site-title">HybridSearch.ai</h1>
      </div>
    </div>
  </header>
</div>

<main className="home-scroll">
 <div className="site-content" id="content">
        <section className="content-intro">
          <div className="inside">
            <h2>Smarter Search Starts Here</h2>
            <p>
              HybridSearch uses AI to understand your meaning and combines it with smart filter
              to bring you the most relevant results, even for complex or conversational queries
            </p>
          </div>
        </section>

        <SearchInput onSearch={handleSearch} />

        {/* Features Section */}
        <section className="infoboxen">
          <div className="inside">
            <h2 className="visually-hidden">Features Overview</h2>

            <article className="infobox">
              <h3>Hybrid Search</h3>
              <p>
                 Search academic literature using natural language and advanced AI to find exactly what you need.
              </p>
            </article>

            <article className="infobox">
              <h3>Summaries</h3>
              <p>
                Get concise and accurate summaries of research articles. No need to read entire papers.
              </p>
            </article>

            <article className="infobox">
              <h3>AI Assistant</h3>
              <p>
               Ask detailed questions and receive clear explanations instantly with our AI assistant.
              </p>
            </article>
          </div>
        </section>

        {/* Reviews Section */}
        <section className="studentFeedback">
          <div className="inside">
            <h2>Reviews</h2>

            <figure className="studentFeedbackItem">
              <blockquote>
                <p>Revolutionized search</p>
              </blockquote>
              <figcaption>— Anna, Data Scientist</figcaption>
            </figure>

            <figure className="studentFeedbackItem">
              <blockquote>
                <p>Valuable insights!</p>
              </blockquote>
              <figcaption>— Erik, Software Developer</figcaption>
            </figure>

            <figure className="studentFeedbackItem">
              <blockquote>
                <p>Efficient and intuitive</p>
              </blockquote>
              <figcaption>— Tom, Law Student</figcaption>
            </figure>

            <figure className="studentFeedbackItem">
              <blockquote>
                <p>User-Friendly</p>
              </blockquote>
              <figcaption>— Sofia, PhD Student</figcaption>
            </figure>

            <figure className="studentFeedbackItem">
              <blockquote>
                <p>Accurate summaries!</p>
              </blockquote>
              <figcaption>— Peter, PhD Student</figcaption>
            </figure>
          </div>
        </section>
      </div>

</main>
      

     
         <footer className="site-footer">
        <div className="inside">
          <div className="footer-text">HybridSearch.ai – Bachelorprosjekt</div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
