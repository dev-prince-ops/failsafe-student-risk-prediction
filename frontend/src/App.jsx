import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import StudentDetail from './pages/StudentDetail'
import Register from './pages/Register'

const ProtectedRoute = ({ children }) => {
  const token = sessionStorage.getItem('token')
  return token ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login"      element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard"  element={
          <ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/student/:id" element={
          <ProtectedRoute><StudentDetail /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  )
}