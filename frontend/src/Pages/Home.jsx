import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import "./style.css";

export default function Home() {
  const navigate = useNavigate();
  const user = localStorage.getItem("user");

  useEffect(() => {
    if (!user) navigate("/");
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <div className="bg">
      <div className="card home">
        <h1>Welcome 🎉</h1>
        <p>Logged in as:</p>
        <h3>{user}</h3>

        <button onClick={handleLogout}>Logout 🚪</button>
      </div>
    </div>
  );
}