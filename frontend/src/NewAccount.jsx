import { useNavigate } from "react-router-dom";
import React, { useState, useLayoutEffect } from "react";
import axios from "axios";
import mascotte from './assets/avatars/avatar_idea_1.png'
import './styles/LoginForm.css'
import NavBarLogin from "./components/NavBarLogin.jsx";

export default function NewAccount() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password_hash, setPasswordHash] = useState("");
    const [pssw_verif, setPsswVerif] = useState("");
    const [error, setError] = useState("");

    useLayoutEffect(() => {
        document.body.style.overflow = "hidden";
        return () => { document.body.style.overflow = ""; };
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        if (password_hash !== pssw_verif) {
            setError("Les mots de passe ne correspondent pas.");
            return;
        }

        try {
            const check = await axios.post("http://127.0.0.1:8000/check_creds", { username });

            if (check.data.exists === true) {
                setError("Ce nom d'utilisateur est déjà utilisé.");
                return;
            }

            const res = await axios.post("http://127.0.0.1:8000/push_account", {
                username,
                password_hash,
            });

            if (res.data.validate === true) {
                navigate("/login");
            }
        } catch (err) {
            setError(err.response?.data?.detail || "Erreur serveur.");
        }
    };

    const goBack = (e) => {
        e.preventDefault();
        navigate("/");
    };

    const confidentialityPolicy = async (e) => {
        e.preventDefault();
        navigate("#");
    };

    return (
        <div className="page-wrapper">
            {/* LEFT — Mascotte */}
            <div className="left-part-wrapper">
                <div className="pixel-bubble">
                    <span>Oh, une nouvelle tête. J'espère que tu vaux mieux que les autres...</span>
                </div>
                <img className="logo-login" src={mascotte} alt="Lilith mascotte" />
            </div>

            {/* RIGHT — Formulaire */}
            <div className="login-form-wrapper">
                <h1 className="login-title">Rejoins<br />Lilith.</h1>
                <form onSubmit={handleSubmit} className="login-form">
                    <input
                        className="input-field"
                        type="text"
                        placeholder="Nom d'utilisateur"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <input
                        className="input-field"
                        type="password"
                        placeholder="Mot de passe"
                        value={password_hash}
                        onChange={(e) => setPasswordHash(e.target.value)}
                        required
                    />
                    <input
                        className="input-field"
                        type="password"
                        placeholder="Confirmer le mot de passe"
                        value={pssw_verif}
                        onChange={(e) => setPsswVerif(e.target.value)}
                        required
                    />
                    <button type="submit" className="submit-button">
                        Créer mon compte
                    </button>
                    <button type="button" className="newaccount-button" onClick={goBack}>
                        Déjà un compte ? Se connecter
                    </button>
                    <div className="legal-checkbox-wrapper">
                        <input type="checkbox" id="legal-new-account" required/>
                        <label htmlFor="legal-new-account">En continuant, vous reconnaissez la <a onClick={confidentialityPolicy}>Politique de Confidentialité</a> de Lilith et acceptez de recevoir occasionnellement des e-mails de mise à jour produit et promotionnels.</label>
                    </div>
                </form>
                {error && <p style={{ color: "#ff6b6b", fontSize: "13px", margin: "4px 0 0" }}>{error}</p>}
            </div>

          {/*TODO: Enlevez ça et mettre les boutons dans la box du form ça sera plus joli*/}
            <NavBarLogin />
        </div>
    );
}
