import React from "react";
import "../styles/MyPageF/HomePageFolder.css/basis.css";
import "../styles/MyPageF/HomePageFolder.css/content.css";
import "../styles/MyPageF/HomePageFolder.css/feedback.css";
import "../styles/MyPageF/HomePageFolder.css/header.css";
import "../styles/MyPageF/HomePageFolder.css/layout.css";
import "../styles/MyPageF/HomePageFolder.css/layout-modern.css";
import "../styles/MyPageF/HomePageFolder.css/navi-responsive.css";



const HomePage = () => {
  return (
    <div className="home">
      {/* Header */}
      <header className="site-header">
        <div className="inside">
          <div className="wrapper">
            <div className="logo-container">
              <a href="/">
              <img src="/images/logo.HybridSearch.svg" 
                    srcSet="/images/logo.HybridSearch.svg 2x" 
                    alt="Logo" 
                    width="222" 
                    height="36" 
                />
              </a>
              <h1>HybridSearch.ai</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="site-content" id="content">
        {/* Hero Section */}
        <section className="content-intro">
          <div className="inside">
            <h2>AI-powered search engine</h2>
            <p>
              AI-powered tool designed to revolutionize the way you discover
              and engage with information.
            </p>
          </div>
        </section>
              {/* Placeholder for searchbar (using Reviews section) */}
      <section className="studentFeedback">
        <div className="inside">
          <h2>Search Placeholder</h2>
          <h2>Search Placeholder</h2>
          <h2>Search Placeholder</h2>
          <h2>Search Placeholder</h2>
        </div>
      </section>

        

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
