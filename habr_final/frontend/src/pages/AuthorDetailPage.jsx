import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api/client'

export default function AuthorDetailPage(){
  const { id } = useParams()
  const [items, setItems] = useState([])
  useEffect(()=>{ api.get(`/authors/${id}`).then(r=>setItems(r.data)) },[id])
  return (
    <div>
      <h2>Author #{id}</h2>
      <ul>
        {items.map(a=> (
          <li key={a.id}><Link to={`/articles/${a.slug}`}>{a.title}</Link></li>
        ))}
      </ul>
    </div>
  )
}


