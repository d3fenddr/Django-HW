import { useEffect, useState } from 'react'
import api from '../api/client'
import { Link } from 'react-router-dom'

export default function AuthorsPage(){
  const [items, setItems] = useState([])
  useEffect(()=>{ api.get('/authors').then(r=>setItems(r.data)) },[])
  return (
    <div>
      <h2>Authors</h2>
      <ul>
        {items.map(u=> (
          <li key={u.id}><Link to={`/authors/${u.id}`}>{u.username}</Link></li>
        ))}
      </ul>
    </div>
  )
}


