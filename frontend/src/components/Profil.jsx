import React from 'react'
import "../styles/Profil.css"
// Différencie la provenance des messages entre le bot et l'user
function Profil ({avatarUrl, username}) {
    return (
        <div className="profil">
            <img src={avatarUrl} alt={`${username} avatar`} className="avatar"/>
            <span className="username">{username}</span>
        </div>
    )
}
export default Profil