'use client'
import { useState } from 'react'
import api from '../../lib/api'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('resource@example.com')
  const [password, setPassword] = useState('resource123')
  const [error, setError] = useState('')
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await api.post('/auth/login', new URLSearchParams({ username: email, password }))
      localStorage.setItem('token', res.data.token)
      router.push('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Sign in</h2>
      <form onSubmit={handleLogin} className="space-y-4">
        <div>
          <label className="text-sm">Email</label>
          <input className="w-full border rounded px-3 py-2" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div>
          <label className="text-sm">Password</label>
          <input type="password" className="w-full border rounded px-3 py-2" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button className="w-full bg-blue-600 text-white py-2 rounded" type="submit">Login</button>
      </form>
    </div>
  )
}
