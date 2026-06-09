import React, { useState } from "react";

function InputBar({ onSend }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your question..."
        style={styles.input}
      />
      <button type="submit" style={styles.button}>
        Send
      </button>
    </form>
  );
}

const styles = {
  form: {
    display: "flex",
    borderTop: "1px solid #ccc",
  },
  input: {
    flex: 1,
    padding: "10px",
    border: "none",
    outline: "none",
  },
  button: {
    padding: "10px 16px",
    background: "#007bff",
    color: "#fff",
    border: "none",
    cursor: "pointer",
  },
};

export default InputBar;