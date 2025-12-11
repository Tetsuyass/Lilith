import { Routes, Route } from "react-router-dom";
import Login from "./Login.jsx";
import App from "./App.jsx";
import NewAccount from "./NewAccount.jsx";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/app" element={<App />} />
      <Route path="/create_account" element={<NewAccount />} />
    </Routes>
  );
}
