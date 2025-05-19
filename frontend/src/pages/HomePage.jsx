// Dette er startsiden for HybridSearch. Den viser søkefelt, introduksjon, funksjonsoversikt og brukeranmeldelser.
// Søket sender brukeren videre til dashboardet eller en personlig side (avhengig av innloggingstilstand).

import React from "react";
import { useNavigate } from "react-router-dom";
import SearchInput from "../components/SearchInput";
import Header from "../components/Header";
import "../assets/styles/HomePage.css";

const HomePage = () => {
  const navigate = useNavigate();
  const userisloggedIn = false; // TODO: Update this logic

  const handleSearch = (query) => {
    const encoded = encodeURIComponent(query);
    if (userisloggedIn) {
      navigate(`/mypage?query=${encoded}`);
      console.log("Navigating to my page. query=" + query);
    } else {
      navigate(`/MyDashboard?query=${encoded}`);
      console.log("Navigating to search page. query=" + query);
    }
  };

  return (
    <div className="home">
      {/* Header */}
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

      {/* Main content */}
      <main className="home-scroll">
        <div className="site-content" id="content">
          {/* Intro */}
          <section className="content-intro">
            <div className="inside">
              <h2>Smarter Search Starts Here</h2>
              <p>
                HybridSearch uses AI to understand your meaning and combines it with smart filters
                to bring you the most relevant results, even for complex or conversational queries.
              </p>
            </div>
          </section>

          {/* Search */}
          <SearchInput onSearch={handleSearch} />

          {/* Features */}
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

          {/* Reviews */}
          <section className="studentFeedback">
            <div className="inside">
              <h2>Reviews</h2>

              {[
                { quote: "Revolutionized search", author: "Anna, Data Scientist" },
                { quote: "Valuable insights!", author: "Erik, Software Developer" },
                { quote: "Efficient and intuitive", author: "Tom, Law Student" },
                { quote: "User-Friendly", author: "Sofia, PhD Student" },
                { quote: "Accurate summaries!", author: "Peter, PhD Student" },
              ].map((item, i) => (
                <figure className="studentFeedbackItem" key={i}>
                  <blockquote>
                    <p>{item.quote}</p>
                  </blockquote>
                  <figcaption>— {item.author}</figcaption>
                </figure>
              ))}
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="site-footer">
        <div className="inside">
          <div className="footer-text">HybridSearch.ai – Bachelorprosjekt</div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
