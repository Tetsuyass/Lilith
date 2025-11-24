import React from 'react'
import '../styles/HistoryItem.css'

function HistoryItem({words}) {

    function onDelete () {
        console.log('Supprimer item')
    }

    return (
        <div className="history-item-container">
            <h3 className="history-item-description">{words}</h3>
            <button className="history-item-delete"
            onClick={onDelete}>X</button>
        </div>
    )
}

export default React.memo(HistoryItem)