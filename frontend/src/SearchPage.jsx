import React, { useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners"; // Import spinner component

const SearchPage = () => {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.get(`http://127.0.0.1:5001/ai-search`, {
        params: { query }
      });

      console.log("Backend Response:", response.data); // Log the raw response

      setResult(response.data);
    } catch (err) {
      setError(
        "Failed to fetch results. Make sure Flask and Ollama are running."
      );
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>AI-Powered Search</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter search query..."
        style={{ padding: "10px", width: "60%" }}
      />
      <button
        onClick={handleSearch}
        style={{ marginLeft: "10px", padding: "10px" }}
      >
        Search
      </button>

      {loading && (
        <div style={{ marginTop: "20px" }}>
          <ClipLoader size={50} color={"#123abc"} loading={loading} />
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div
          style={{
            marginTop: "20px",
            textAlign: "left",
            maxWidth: "600px",
            margin: "0 auto"
          }}
        >
          <h3>Selected Article:</h3>
          <p>
            <strong>Title:</strong> {result.article.title}
          </p>
          <p>
            <strong>Abstract:</strong> {result.article.abstract}
          </p>
          <p>
            <strong>Author(s):</strong> {result.article.author}
          </p>
          <p>
            <strong>Publication Date:</strong> {result.article.publication_date}
          </p>

          <h3>AI Summary:</h3>
          <p>{result.ai_summary}</p>

          {/* Check if pdf_url exists and show it */}
          {result.article.pdf_url && (
            <div>
              <h3>Download PDF:</h3>
              <a
                href={result.article.pdf_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Click here to download the PDF
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchPage;
