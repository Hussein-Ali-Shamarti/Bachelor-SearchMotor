// Denne komponenten lar brukeren chatte med en AI-assistent om en valgt artikkel.
// Den viser tidligere meldinger og håndterer sending av spørsmål via API-kall.
// Meldinger kan sendes med Enter-tasten eller via en knapp.


import React, { useState } from "react";
import axios from "axios";
import EnterIcon from "../assets/images/Eenter.svg";

function ChatSection({ selectedArticle, chatHistory, setChatHistory }) {
  const [chatMessage, setChatMessage] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  const sendChatMessage = async () => {
    if (!chatMessage.trim() || !selectedArticle) return;
    const userMsg = chatMessage.trim();

    setChatHistory((prev) => [...prev, { sender: "user", message: userMsg }]);
    setChatMessage("");
    setChatLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:5001/chat", {
        article_id: selectedArticle.id,
        message: userMsg,
      });

      if (response.data.answer) {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: response.data.answer },
        ]);
      } else if (response.data.error) {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: "Error: " + response.data.error },
        ]);
      }
    } catch (err) {
      console.error(err);
      setChatHistory((prev) => [
        ...prev,
        {
          sender: "bot",
          message: "Failed to send message. Please try again.",
        },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !chatLoading && chatMessage.trim()) {
      e.preventDefault();
      sendChatMessage();
    }
  };

  return (
    <aside className="ai-sidebar">
      <div className="ai-squish-container">
        <h3>Chat about this article</h3>

        {!selectedArticle ? (
          <p>Please select an article to start chatting.</p>
        ) : (
          <div className="chat-container">
            <div className="chat-history">
              {chatHistory.length === 0 && (
                <p>No messages yet. Start the conversation!</p>
              )}
              {chatHistory.map((entry, index) => (
                <div
                  key={index}
                  className={`chat-message ${
                    entry.sender === "user" ? "user-message" : "bot-message"
                  }`}
                >
                  <strong>{entry.sender === "user" ? "You:" : "Bot:"}</strong>{" "}
                  {entry.message}
                </div>
              ))}
            </div>

            <div className="search-wrapper">
              <input
                type="text"
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about the article..."
                className="search-input"
                disabled={!selectedArticle}
              />
              <button
                type="button"
                onClick={sendChatMessage}
                className="Enter-icon"
                disabled={!selectedArticle || chatLoading || !chatMessage.trim()}
              >
                <img src={EnterIcon} alt="Send" />
              </button>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}

export default ChatSection;
