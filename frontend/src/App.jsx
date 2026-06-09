import React, { useState, useRef, useEffect } from 'react';
import { sendMessage } from './api/chat';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'bot',
      text: 'Hello! I\'m the ICICI Pru Life FAQ Assistant. How can I help you today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatContext, setChatContext] = useState(null);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMsg = { id: Date.now(), role: 'user', text: trimmed };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const data = await sendMessage(trimmed, chatContext);
      const botMsg = { id: Date.now() + 1, role: 'bot', text: data.answer };
      setMessages(prev => [...prev, botMsg]);
      // Persist chat_context for multi-turn conversations
      if (data.chat_context) setChatContext(data.chat_context);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-logo">💬</div>
        <div>
          <h1>ICICI Pru Life FAQ Assistant</h1>
          <p>Powered by Neuro-SAN</p>
        </div>
      </header>

      <div className="chat-window">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="bubble">{msg.text}</div>
          </div>
        ))}

        {loading && (
          <div className="message bot">
            <div className="bubble typing">
              <span /><span /><span />
            </div>
          </div>
        )}

        {error && (
          <div className="error-banner">⚠️ {error}</div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="input-bar">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your question here... (Enter to send)"
          disabled={loading}
          rows={1}
        />
        <button onClick={handleSend} disabled={loading || !input.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}

export default App;