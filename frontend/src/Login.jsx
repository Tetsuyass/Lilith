import React, {useState} from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import './styles/LoginForm.css'

export default function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password_hash, setPasswordHash] = useState("");
    const [error, setError] = useState("");
    const [token, setToken] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    //setError("");

    //try {
      //const response = await axios.post("http://127.0.0.1:8000/login", {
        //username,
        //password_hash,
      //});

      //setToken(response.data.access_token);
    //} catch (err) {
      //setError(err.response?.data?.detail || "Erreur serveur");
    //}
    localStorage.setItem("token", "dummy_token");

    navigate("/app"); // redirection vers ta vraie App
  };

  const createAccount = async (e) => {
      e.preventDefault();
      setError("");

      navigate("/create_account")
  };

  return (
      <div className="login-form-wrapper">
          <h2 className="login-form-wrapper-title">Connexion</h2>
          <form onSubmit={handleSubmit} className="login-form">
                <input className="input-field" type="text"
                placeholder="Username"
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
          </form>
          {error && <p style={{ color: "red" }}>{error}</p>}
          {token && <p style={{ color: "green" }}>Connecté ! Token : {token}</p>}
      </div>
  )
}