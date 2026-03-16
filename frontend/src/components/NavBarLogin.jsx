import "../styles/NavBarLogin.css"
import logo from "../assets/avatars/lilith1.jpeg";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function NavBarLogin() {
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const discoverLilith = async (e) => {
      e.preventDefault();
      setError("");
      //TODO : A changer

      navigate("/#")
  }

  const tarifications = async (e) => {
      e.preventDefault();
      setError("");
      //TODO : A changer

      navigate("#")
  }

    const contactComm = async (e) => {
      e.preventDefault();
      setError("");
      //TODO : A changer

      navigate("#")
  }

    const tryLilith = async (e) => {
      e.preventDefault();
      setError("");
      //TODO : A changer

      navigate("#")
  }
    return (
        <div className="navbar-login">
            <div className="navbar-login-row" id="navbar-login-row-1">
                <img className="logo-app" src={logo} alt="Lilith logo"/>
                <p>Lilith</p>
                <a onClick={discoverLilith}>Découvrez Lilith</a>
                <a onClick={tarifications}>Tarifications</a>
                <a onClick={contactComm}>Contactez-nous</a>
                <a onClick={tryLilith}>Essayer Lilith</a>
            </div>
        </div>
    );
}