import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./style.css";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("https://auth-ye7t.onrender.com/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    setMessage(data.message);

    if (data.status === "success") {
      setTimeout(() => navigate("/"), 1000);
    }
  };

  return (
    <div className="bg fun">
      <div className="card glow">
        <h2>Create Account ✨😎</h2>

        <form onSubmit={handleSubmit}>
          <input name="username" placeholder="👤 Username" onChange={handleChange} />
          <input name="email" placeholder="📧 Email" onChange={handleChange} />
          <input
            name="password"
            type="password"
            placeholder="🔐 Password"
            onChange={handleChange}
          />
          <button>Join Now 🎉</button>
        </form>

        <p className="msg">{message}</p>

        <span onClick={() => navigate("/")}>
          Already user? Login 🔐
        </span>
      </div>
    </div>
  );
}