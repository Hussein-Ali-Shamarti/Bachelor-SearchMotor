import React from "react";

function SidebarAI({ toggleAiSidebar, isHidden }) {
  return (
    <aside className={`ai-sidebar ${isHidden ? "hidden" : "active"}`}>
      <div className="ai-sidebar-panel">
        <button onClick={toggleAiSidebar} className="ai-close-button-mobile">
          Close ✖
        </button>

        <div className="chat-container">
          <h3>Chat about this article</h3>
          <p>This is where the chat content will appear.</p>
        </div>
      </div>
    </aside>
  );
}

export default SidebarAI;
