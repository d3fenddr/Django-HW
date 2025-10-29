import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'

export default function SignupPage(){
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  return (
    <div className="d-flex justify-content-center">
      <div className="card shadow-sm" style={{maxWidth:540, width:'100%'}}>
        <div className="card-body">
          <h4 className="mb-4">Регистрация</h4>
          {error && <div className="alert alert-danger py-2" role="alert">{error}</div>}
          <form onSubmit={async e=>{
            e.preventDefault();
            setError('');
            if(password !== confirm){ setError('Пароли не совпадают'); return }
            setLoading(true)
            try {
              await api.post('/auth/register', {username, email, password})
              window.location.href = '/login'
            } catch (err) {
              setError('Не удалось зарегистрироваться')
            } finally {
              setLoading(false)
            }
          }}>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input className="form-control" type="email" placeholder="you@example.com" value={email} onChange={e=>setEmail(e.target.value)} required />
            </div>
            <div className="mb-3">
              <label className="form-label">Никнейм</label>
              <input className="form-control" placeholder="nickname" value={username} onChange={e=>setUsername(e.target.value)} required />
            </div>
            <div className="mb-3">
              <label className="form-label">Пароль</label>
              <input className="form-control" type="password" placeholder="••••••••" value={password} onChange={e=>setPassword(e.target.value)} required />
            </div>
            <div className="mb-3">
              <label className="form-label">Пароль ещё раз</label>
              <input className="form-control" type="password" placeholder="••••••••" value={confirm} onChange={e=>setConfirm(e.target.value)} required />
            </div>
            <div className="form-check mb-2">
              <input className="form-check-input" type="checkbox" id="agree1" required />
              <label className="form-check-label" htmlFor="agree1">Я принимаю условия Пользовательского соглашения</label>
            </div>
            <div className="form-check mb-3">
              <input className="form-check-input" type="checkbox" id="agree2" required />
              <label className="form-check-label" htmlFor="agree2">Я согласен на обработку персональных данных</label>
            </div>
            <button className="btn btn-primary w-100" disabled={loading}>{loading ? 'Регистрируем…' : 'Регистрация'}</button>
          </form>
        </div>
        <div className="card-footer bg-white text-center">
          Уже зарегистрированы? <Link to="/login">Войдите</Link>
        </div>
      </div>
    </div>
  )
}


