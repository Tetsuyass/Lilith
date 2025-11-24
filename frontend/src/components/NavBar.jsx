import React from 'react'
import '../styles/NavBar.css'
import settingsUrl from '../assets/settings_logo.png'
import newChatUrl from '../assets/new_chat_logo.png'

function NavBar({ version, appName }) {
    return (
        <div className="navbar">

            <div className="navbar-left">
                <img src={settingsUrl} className="icon" alt="Settings logo" />
                <img src={newChatUrl} className="icon" alt="New Chat logo"/>
            </div>

            <p className="app-name">{appName}</p>

            <p className="version">{version}</p>
        </div>
    )
}

export default NavBar
