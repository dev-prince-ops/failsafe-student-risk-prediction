import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

export default function Login() {
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const nav = useNavigate()

  const handleLogin = async () => {
    setError('')
    try {
      const form = new FormData()
      form.append('username', email)
      form.append('password', password)
      const res = await api.post('/auth/login', form)
      sessionStorage.setItem('token', res.data.access_token)
      nav('/dashboard')
    } catch {
      setError('Invalid email or password')
    }
  }

  return (
    <div style={{maxWidth:360,margin:'80px auto',padding:'2rem',
      border:'0.5px solid #e0e0e0',borderRadius:12}}>
      <h2 style={{marginBottom:'1.5rem',fontSize:20}}>FAILSAFE — sign in</h2>
      <input type="email" placeholder="Email"
        value={email} onChange={e=>setEmail(e.target.value)}
        style={{width:'100%',marginBottom:10}} />
      <input type="password" placeholder="Password"
        value={password} onChange={e=>setPassword(e.target.value)}
        style={{width:'100%',marginBottom:16}} />
      {error && <p style={{color:'#D85A30',fontSize:13,marginBottom:10}}>{error}</p>}
      <button
        onClick={handleLogin}
        style={{width:'100%', marginBottom:'10px'}}
      >
        Sign in
      </button>

      <button
        onClick={() => nav('/register')}
        style={{width:'100%'}}
      >
        Register
      </button>
    </div>
  )
}