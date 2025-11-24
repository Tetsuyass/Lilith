import React, { useState } from 'react';
import '../styles/QueryZone.css';

function QueryZone({ onSend }) {
  const [query, setQuery] = useState('');

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && query.trim() !== '') {
      onSend(query);   // envoie le message au parent
      setQuery('');    // vide l'input
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
    </div>
  );
}

export default QueryZone;
