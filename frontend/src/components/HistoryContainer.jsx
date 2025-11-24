import React, {useEffect, useRef} from 'react'
import '../styles/HistoryContainer.css'
import HistoryItem from "./HistoryItem.jsx";

function HistoryContainer({tokens = [], words = []}) {
    const containerRef = useRef(null);

    useEffect(() => {
      if (containerRef.current) {
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
      }
    }, [tokens]);
    return (
        <div className="history-container" ref={containerRef}>
            <h2 className="history-container-title">Historique des conversations</h2>
            <div className="history-title-container"></div>
            {tokens.map((tok, index) => (
                <HistoryItem
                    words={words}
                />
            ))}
            <p>CECI EST UN TEST AVEC BEAUCOUP DE MOTS BLABLABLA HAHAHAHAHAHA POUR VOIR JUSQUOU CET ENFANT DE FLEXBOX
                PEUT ALLER REGARDER ON DIRAIT UN TROUBADOUR HAHAHAH</p>
        </div>
    )
}

export default HistoryContainer