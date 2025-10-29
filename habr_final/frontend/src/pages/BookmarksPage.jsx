import { useEffect, useState } from 'react'
import api from '../api/client'
import { Link } from 'react-router-dom'

export default function BookmarksPage(){
  const [items, setItems] = useState([])
  useEffect(()=>{ api.get('/bookmarks').then(r=>setItems(r.data)) },[])
  return (
    <div>
      <h2 className="mb-3">Закладки</h2>
      <div className="list-group">
        {items.map(a=> (
          <Link key={a.id} to={`/articles/${a.slug}`} className="list-group-item list-group-item-action">{a.title}</Link>
        ))}
      </div>
    </div>
  )
}


