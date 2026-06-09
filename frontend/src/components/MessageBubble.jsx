import React from "react";

function MessageBubble({ message }) {
  const isUser = message.sender === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "8px",
      }}
    >
      <div
        style={{
          background: isUser ? "#007bff" : "#e9ecef",
          color: isUser ? "#fff" : "#000",
          padding: "8px 12px",
          borderRadius: "12px",
          maxWidth: "70%",
        }}
      >
        {message.text}
      </div>
    </div>
  );
}

export default MessageBubble;