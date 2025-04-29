import React, { useEffect } from "react";
import "../assets/styles/MyDashboard.css"; 
import HeaderMyDashboard from "../components/HeaderMyDashboard";

function MyDashboard() {
  useEffect(() => {
    const leftButton = document.querySelector('.sidebar-left-toggle');
    const rightButton = document.querySelector('.sidebar-right-toggle');

    const toggleLeft = () => {
      document.querySelector('.nav-sidebar').classList.toggle('hidden');
    };

    const toggleRight = () => {
      document.querySelector('.ai-sidebar').classList.toggle('hidden');
    };

    if (leftButton) leftButton.addEventListener('click', toggleLeft);
    if (rightButton) rightButton.addEventListener('click', toggleRight);

    return () => {
      if (leftButton) leftButton.removeEventListener('click', toggleLeft);
      if (rightButton) rightButton.removeEventListener('click', toggleRight);
    };
  }, []);

  return (
    <div className="outer-wrap">
      
      {/* Header */}
      <HeaderMyDashboard /> 

      <div className="dashboard">
        <aside className="nav-sidebar">
          {/* Meny */}
          <div className="nav-squish-container">
            <h3>Explore:</h3>
            <nav className="example-menu">
              <ul>
                <li><a href="#">Search History</a></li>
                <li><a href="#">Search History</a></li>
                <li><a href="#">Search History</a></li>
                <li><a href="#">Search History</a></li>
              </ul>
            </nav>
          </div>

          {/* Login + Registration knappene flyttes hit */}
          <div className="auth-buttons-sidebar">
            <button className="auth-button">Login</button>
            <button className="auth-button">Registration</button>
          </div>
        </aside>

        <main className="main-area">
          <article className="post-content">
            <h2>gammel</h2>
            <p>ikke slett enda - noe struktur styling er fra her... </p>
            
            <p>...</p>
          </article>
        </main>

        <aside className="ai-sidebar">
          <div className="ai-squish-container">
            <h3>AI Tools:</h3>
            <nav className="example-menu">
              <ul>
                <li><a href="#">AI chat kommer her</a></li>
                <li><a href="#">og summary / svar under her? </a></li>
              </ul>
            </nav>
          </div>
        </aside>
      </div>

      <footer className="footer-area">
        <p>Evt. popup her til høyre (?)</p>
      </footer>
    </div>
  );
}

export default MyDashboard;
