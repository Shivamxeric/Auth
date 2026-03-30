import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "./style.css";

export default function Home() {
      const navigate = useNavigate();
      const [user, setUser] = useState("");

      const token = localStorage.getItem("token");

      useEffect(() => {
        const token = localStorage.getItem("token");
      
        if (!token) {
          navigate("/");
          return;
        }
      
        fetch("https://auth-ye7t.onrender.com/home/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
    .then(res => res.json())
    .then(data => {
      if (data.status !== "success") {
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
