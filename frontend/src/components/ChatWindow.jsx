import React, { useState } from "react";
import NavBar from "./NavBar";
import ChatContainer from "./ChatContainer";
import QueryZone from "./QueryZone";
import "../styles/ChatWindow.css";
import avatarBot from '../assets/avatars/lilith1.jpeg';
import avatarUser from '../assets/avatars/user.jpg';
import api from "../hooks/api.js";


function ChatWindow() {
  const user_session_username = "Ismael";
  const [messages, setMessages] = useState([
    { author: "lilith", username: "Lilith", avatarUrl: avatarBot, text: "Bonjour " + user_session_username + "." }
  ]);

const handleSend = async (text) => {
  setMessages(prev => [
    ...prev,
    { author: "user", username: "Tetsuya 乂", avatarUrl: avatarUser, text }
  ]);
  setMessages(prev => [
  ...prev,
  {
    author: "lilith",
    username: "Lilith",
    avatarUrl: avatarBot,
    text: "En train d'écrire...",
    typing: true,
  }
  ]);
  try {
    const response = await api.post("/chat", { user_message: text });


  const fullText = response.data.reply;
  let index = 0;

  setMessages(prev => prev.filter(msg => !msg.typing));  //supprime l'état typing

  setMessages(prev => [  //ajouter un message vide du bot pour streaming
    ...prev,
    {
      author: "lilith",
      username: "Lilith",
      avatarUrl: avatarBot,
      text: "",
      streaming: true,
    }
  ]);

  // Streaming
  const interval = setInterval(() => {
    index++;

    setMessages(prev =>
      prev.map(msg =>
        msg.streaming
          ? { ...msg, text: fullText.slice(0, index) }
          : msg
      )
    );

    if (index >= fullText.length) {
      clearInterval(interval);

      // Nettoyage du flag streaming
      setMessages(prev =>
        prev.map(msg =>
          msg.streaming ? { ...msg, streaming: false } : msg
        )
      );
    }
  }, 20); // vitesse du streaming (ms par caractère)


  } catch (err) {
    console.error(err);

    setMessages(prev => prev.filter(msg => !msg.typing));  //supprime l'état typing
    setMessages(prev => [
      ...prev,
      { author: "lilith", username: "Lilith", avatarUrl: avatarBot, text: "Le serveur ne répond pas, merci de réessayer ultérieurement." }
    ]);
  }
};

  return (
    <div className="chat-window">
      <NavBar
        appName="Lilith"
        version="v1.0"
      />
      <ChatContainer messages={messages} />
      <QueryZone onSend={handleSend} />
    </div>
  );
}

export default ChatWindow;
