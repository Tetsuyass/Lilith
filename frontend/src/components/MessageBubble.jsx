import React from "react";
import Profil from "./Profil";
import TypingDots from "./TypingDots";
import "../styles/MessageBubble.css";

function MessageBubble({ author, avatarUrl, username, text, typing }) {
    return (
        <div className={`message-bubble ${author}`}>
            <Profil avatarUrl={avatarUrl} username={username} />

            <div className="message-text">
                {typing ? <TypingDots /> : text}
            </div>
        </div>
    );
}

export default MessageBubble;
