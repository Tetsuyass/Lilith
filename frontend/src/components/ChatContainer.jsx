import React, { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import "../styles/ChatContainer.css";
function ChatContainer({ messages }) {
  const containerRef = useRef(null);

  // Scroll automatique vers le bas à chaque nouveau message
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="chat-container" ref={containerRef}>
      {messages.map((msg, index) => (
        <MessageBubble
          key={index}
          author={msg.author}
          username={msg.username}
          avatarUrl={msg.avatarUrl}
          text={msg.text}
          typing={msg.typing}
        />
      ))}
    </div>
  );
}

export default ChatContainer;
