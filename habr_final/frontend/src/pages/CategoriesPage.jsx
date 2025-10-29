import { useEffect, useState } from 'react'
import api from '../api/client'
import { Link } from 'react-router-dom'

export default function CategoriesPage(){
  const [cats, setCats] = useState([])
  useEffect(()=>{ api.get('/categories').then(r=>setCats(r.data)) },[])
  return (
    <div>
      <h2>Categories</h2>
      <ul>
        {cats.map(c=> (
          <li key={c.id}>{c.name}</li>
        ))}
      </ul>
    </div>
  )
}


