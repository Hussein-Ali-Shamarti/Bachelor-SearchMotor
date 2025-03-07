import React from "react";
import SearchInput from "../components/SearchInput";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import "../assets/styles/HomePage.css";


const HomePage = () => {
  const navigate = useNavigate();
  const userisloggedIn = false; // TODO: Oppdater denne logikken

  const handleSearch = (query) => {
    if (userisloggedIn) {
      navigate(`/mypage?query=${encodeURIComponent(query)}`);
      console.log("Navigating to my page. query=" + query);
    } else {
      navigate(`/search?query=${encodeURIComponent(query)}`);
      console.log("Navigating to search page. query=" + query);
    }
  };

  return (
    <div className="home">
      <Header />

      {/* Bruker eksisterende stil for knapper */}
      <div className="auth-buttons" style={{ textAlign: "right", padding: "10px" }}>
        <button onClick={() => navigate("/login")} className="button">
          Login
        </button>
        <button onClick={() => navigate("/register")} className="button">
          Registration
        </button>
      </div>

      <main className="site-content" id="content">
        <section className="content-intro">
          <div className="inside">
            <h2>AI-powered search engine</h2>
            <p>
              AI-powered tool designed to revolutionize the way you discover
              and engage with information.
            </p>
          </div>
        </section>

        <SearchInput onSearch={handleSearch} />

        {/* Features Section */}
        <section className="infoboxen">
          <div className="inside">
            <h2 className="visually-hidden">Features Overview</h2>

            <article className="infobox">
              <h3>Getting Started</h3>
              <p>
                Essential insights and step-by-step guidance to help you begin
                your journey with HybridSearch.ai.
              </p>
              <p>
                <a href="..." className="button">
                  Discover more
                </a>
              </p>
            </article>

            <article className="infobox">
              <h3>Efficient Search</h3>
              <p>
                Our intelligent algorithms provide you with the most relevant
                information quickly.
              </p>
              <p>
                <a href="..." className="button">
                  Discover more
                </a>
              </p>
            </article>

            <article className="infobox">
              <h3>AI Chat</h3>
              <p>
                It's your personal assistant for data exploration and analysis,
                right at your fingertips.
              </p>
              <p>
                <a href="..." className="button">
                  Discover more
                </a>
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
      </main>

      {/* Footer */}
      <footer className="site-footer">
        <div className="inside">
          <nav className="footer-nav">
            <ul>
              <li>
                <a href="#">Legal Notice</a>
              </li>
              <li>
                <a href="#">Privacy Protection</a>
              </li>
              <li>
                <a href="#top">Back to top</a>
              </li>
            </ul>
          </nav>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
