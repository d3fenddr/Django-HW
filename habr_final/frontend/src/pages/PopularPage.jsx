import { useEffect, useState } from 'react'
import api from '../api/client'
import { Link } from 'react-router-dom'

export default function PopularPage(){
  const [items, setItems] = useState([])
  useEffect(()=>{ api.get('/articles/popular').then(r=>setItems(r.data)) },[])
  return (
    <div>
      <h2 className="mb-3">Популярное</h2>
      <div className="list-group">
        {items.map(a=> (
          <Link key={a.id} to={`/articles/${a.slug}`} className="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
            <span>{a.title}</span>
            <span className="badge text-bg-info">{(a.rating_avg||0).toFixed(1)}/5</span>
          </Link>
        ))}
      </div>
    </div>
  )
}


