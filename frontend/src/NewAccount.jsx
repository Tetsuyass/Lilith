import {useNavigate} from "react-router-dom";
import React, {useState} from "react";
import axios from "axios";
import './styles/LoginForm.css'

export default function NewAccount() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password_hash, setPasswordHash] = useState("");
  const [pssw_verif, setPsswVerif] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (password_hash !== pssw_verif) {
      setError("Les mots de passe ne correspondent pas.");
      return;
    }

    try {
      // Vérifier si le username existe déjà
      const check = await axios.post("http://127.0.0.1:8000/check_creds", {
        username,
      });

      if (check.data.exists === true) {
        setError("Ce nom d'utilisateur est déjà utilisé.");
        return;
      }

      // Création du compte
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

  return (
    <div className="login-form-wrapper">
      <h2 className="login-form-wrapper-title">Créer un compte</h2>

      <form onSubmit={handleSubmit} className="login-form">
        <input
          className="input-field"
          type="text"
          placeholder="Username"
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
          placeholder="Vérifiez votre mot de passe"
          value={pssw_verif}
          onChange={(e) => setPsswVerif(e.target.value)}
          required
        />

        <button type="submit" className="newaccount-button">
          Créer mon compte
        </button>
      </form>

      {error && <p style={{color: "red"}}>{error}</p>}
    </div>
  );
}
