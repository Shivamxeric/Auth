import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./style.css";
import { toast } from "react-toastify"; 

export default function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

 const handleSubmit = async (e) => {
  e.preventDefault();

  const res = await fetch("http://127.0.0.1:8000/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(form),
  });

  const data = await res.json();

  if (data.status === "success") {
    toast.success("Login Successful 🎉");
    localStorage.setItem("user", form.email);

    setTimeout(() => navigate("/home"), 1500);
  } else {
    toast.error(data.message);
  }
};

  return (
    
    <div className="bg">
      <div className="card">
        <h2>Welcome Back 🔐</h2>

        <form onSubmit={handleSubmit}>
          <input name="email" placeholder="📧 Email" onChange={handleChange} />
          <input
            name="password"
            type="password"
            placeholder="🔒 Password"
            onChange={handleChange}
          />
          <button>Login 🚀</button>
        </form>

        <p className="msg">{message}</p>

        <span onClick={() => navigate("/register")}>
          New user? Register 😎
        </span>
      </div>   
    </div> 

  ); 
}     
         
 
  