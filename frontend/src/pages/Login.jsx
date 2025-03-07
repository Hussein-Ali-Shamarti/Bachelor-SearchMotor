import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import "../FirebaseConfig";
import "../assets/styles/Login.css"; // Importerer stil

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const auth = getAuth();

  const handleSignIn = async (event) => {
    event.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      alert("Login successful!");
      navigate("/MyPage");
    } catch (error) {
      console.error("Error during login:", error);
      alert("Login failed: " + error.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Welcome back</h2>
      <form onSubmit={handleSignIn}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <div className="login-buttons">
          <button type="submit">Login</button>
          <button onClick={() => navigate("/register")} type="button">
            New user
          </button>
        </div>
        <a href="/forgot-password" className="forgot-password">
          Forgot your password?
        </a>
      </form>
    </div>
  );
};

export default Login;
