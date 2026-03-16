import React, {useState, useLayoutEffect} from 'react';
import { useNavigate } from "react-router-dom";
import mascotte from './assets/avatars/avatar_idea_1.png'
import axios from 'axios';
import './styles/LoginForm.css'
import NavBarLogin from "./components/NavBarLogin.jsx";

export default function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password_hash, setPasswordHash] = useState("");
    const [error, setError] = useState("");
    const [token, setToken] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        localStorage.setItem("token", "dummy_token");
        navigate("/app");
    };

    useLayoutEffect(() => {
        document.body.style.overflow = "hidden";
        return () => { document.body.style.overflow = ""; };
    }, []);

    const createAccount = async (e) => {
        e.preventDefault();
        navigate("/create_account");
    };

    const confidentialityPolicy = async (e) => {
        e.preventDefault();
        navigate("/#");
    };

    return (
        <div className="page-wrapper">
            {/* LEFT — Mascotte collée en bas */}
            <div className="left-part-wrapper">
                {/* Bulle pixel art */}
                <div className="pixel-bubble">
                    <span>Encore toi ? À croire que tu es amoureux...</span>
                </div>
                <img className="logo-login" src={mascotte} alt="Lilith mascotte"/>
            </div>

            {/* RIGHT — Formulaire centré verticalement */}
            <div className="login-form-wrapper">
                <h1 className="login-title">L'IA pensée<br/>pour vous.</h1>
                <form onSubmit={handleSubmit} className="login-form">
                    <input className="input-field" type="text"
                           placeholder="Adresse e-mail"
                           value={username}
                           onChange={(e) => setUsername(e.target.value)}
                    />
                    <input className="input-field" type="password"
                           placeholder="Mot de passe"
                           value={password_hash}
                           onChange={(e) => setPasswordHash(e.target.value)}
                    />
                    <button type="submit" className="submit-button">
                        Se connecter
                    </button>
                    <button type="button" className="newaccount-button" onClick={createAccount}>
                        Créer un compte
                    </button>
                    <p className="legal-mention-login">
                        En continuant, vous reconnaissez la{" "}
                        <a onClick={confidentialityPolicy} className="hypertext-link">
                            Politique de Confidentialité
                        </a>{" "}
                        de Lilith et acceptez de recevoir occasionnellement des e-mails de mise à jour produit et promotionnels.
                    </p>
                </form>
                {error && <p style={{color: "red"}}>{error}</p>}
                {token && <p style={{color: "green"}}>Connecté !</p>}
            </div>

            <NavBarLogin />
        </div>
    );
}
