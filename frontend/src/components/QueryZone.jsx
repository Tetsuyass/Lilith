import React, { useState } from 'react';
import '../styles/QueryZone.css';
import envoyerIcon from '../assets/envoyer.png';

function QueryZone({ onSend }) {
  const [query, setQuery] = useState('');

  const sendMessage = () => {
    if (query.trim() === '') return;  // n'envoie pas les messages vides

    onSend(query);   // envoie le message au parent
    setQuery('');    // vide le champ
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="query-zone">
      <input
        name="query"
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Tape ton message..."
      />
      <button onClick={sendMessage} className="query-submit-button">
        <img src={envoyerIcon} alt="Envoyer" />
      </button>
    </div>
  );
}

export default QueryZone;
