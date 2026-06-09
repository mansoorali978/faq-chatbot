import React, { useState } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";
import { sendMessage } from "../api/chat";

function ChatWindow() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    const userMessage = { text, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const reply = await sendMessage(text);
      const botMessage = { text: reply, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { text: "Error: Could not get response", sender: "bot" };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>FAQ Chatbot</div>
      <div style={styles.messages}>
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}
      </div>
      <InputBar onSend={handleSend} />
    </div>
  );
}

const styles = {
  container: {
    width: "400px",
    margin: "50px auto",
    border: "1px solid #ccc",
    borderRadius: "8px",
    overflow: "hidden",
    fontFamily: "Arial, sans-serif",
  },
  header: {
    background: "#007bff",
    color: "#fff",
    padding: "12px",
    textAlign: "center",
    fontWeight: "bold",
  },
  messages: {
    height: "400px",
    overflowY: "auto",
    padding: "10px",
    background: "#f9f9f9",
  },
};

export default ChatWindow;