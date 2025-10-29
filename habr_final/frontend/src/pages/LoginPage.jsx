import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'

export default function LoginPage(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  return (
    <div className="d-flex justify-content-center">
      <div className="card shadow-sm" style={{maxWidth:480, width:'100%'}}>
        <div className="card-body">
          <h4 className="mb-4">Вход</h4>
          {error && <div className="alert alert-danger py-2" role="alert">{error}</div>}
          <form onSubmit={async e => {
            e.preventDefault()
            setError('')
            setLoading(true)
            try {
              const r = await api.post(
                '/auth/login',
                {
                  username: username,
                  password: password
                },
                {
                  headers: {
                    'Content-Type': 'application/json'
                  }
                }
              )
              localStorage.setItem('habr_token', r.data.access_token)
              window.location.href = '/'
            } catch (err) {
              setError('Неверные данные для входа')
            } finally {
              setLoading(false)
            }
          }}>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input className="form-control" type="email" placeholder="you@example.com" value={username} onChange={e=>setUsername(e.target.value)} required />
            </div>
            <div className="mb-3">
              <label className="form-label">Пароль</label>
              <input className="form-control" type="password" placeholder="••••••••" value={password} onChange={e=>setPassword(e.target.value)} required />
            </div>
            <button className="btn btn-primary w-100" disabled={loading}>{loading ? 'Входим…' : 'Войти'}</button>
          </form>

          <div className="text-center mt-3">
            <Link to="#" className="small text-muted">Забыли пароль?</Link>
          </div>

          <div className="text-center text-muted mt-3">Или войдите с помощью других сервисов</div>
          <div className="d-flex justify-content-center gap-2 mt-2">
            {["github","vk","google","facebook","x","yandex"].map((k,i)=> (
              <span key={i} className="btn btn-light border" style={{width:40,height:40,display:'inline-flex',alignItems:'center',justifyContent:'center'}}>∎</span>
            ))}
          </div>
        </div>
        <div className="card-footer bg-white text-center">
          Ещё нет аккаунта? <Link to="/signup">Зарегистрируйтесь</Link>
        </div>
      </div>
    </div>
  )
}


