import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "./style.css";

export default function Home() {
      const navigate = useNavigate();
      const [user, setUser] = useState("");

      const token = localStorage.getItem("token");

      useEffect(() => {
      if (!token) {
      navigate("/");
      return;
      }


      fetch("https://auth-ye7t.onrender.com/home/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(res => res.json())
        .then(data => {
          if (data.status === "success") {
            setUser(data.message); // or extract username
          } else {
            localStorage.removeItem("token");
            navigate("/");
          }
        })
        .catch(() => {
          navigate("/");
        });


      }, []);

      const handleLogout = () => {
      localStorage.removeItem("token");
      navigate("/");
      };

      return ( <div className="bg"> <div className="card home"> <h1>Welcome 🎉</h1> <p>{user}</p>

      ```
          <button onClick={handleLogout}>Logout 🚪</button>
        </div>
      </div>
      

      );
      }
