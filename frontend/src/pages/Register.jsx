import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Register() {

  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const nav = useNavigate();

  const register = async () => {

    try {

      await api.post("/auth/register", {
        email,
        name,
        password
      });

      alert("Registration successful");

      nav("/login");

    } catch (err) {

      alert(
        err.response?.data?.detail ||
        "Registration failed"
      );

    }
  };

  return (
    <div style={{padding:"2rem"}}>

      <h1>Register</h1>

      <input
        placeholder="Name"
        value={name}
        onChange={(e)=>setName(e.target.value)}
      />

      <br/><br/>

      <input
        placeholder="Email"
        value={email}
        onChange={(e)=>setEmail(e.target.value)}
      />

      <br/><br/>

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e)=>setPassword(e.target.value)}
      />

      <br/><br/>

      <button onClick={register}>
        Register
      </button>

      <button
        style={{marginLeft:"10px"}}
        onClick={()=>nav("/login")}
      >
        Back to Login
      </button>

    </div>
  );
}