import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api/client'

export default function ArticleDetailPage(){
  const { slug } = useParams()
  const [a, setA] = useState(null)
  useEffect(()=>{ api.get(`/articles/${slug}`).then(r=>setA(r.data)) },[slug])
  if(!a) return <div>Loading...</div>
  return (
    <div className="mb-4">
      <div className="small text-muted mb-2">
        Категория: {a.category?.name || '—'}
      </div>
      <h1 className="mb-3">{a.title}</h1>
      {a.image_url && <img src={a.image_url} alt="" className="img-fluid mb-3" />}
      <div className="lead" style={{whiteSpace:'pre-line'}}>{a.body}</div>

      <div className="d-flex align-items-center gap-2 mt-3">
        <button className="btn btn-outline-success" onClick={()=> api.post('/reactions', {article_id:a.id, value:1}).then(()=> window.location.reload())}>👍 {a.likes}</button>
        <button className="btn btn-outline-danger" onClick={()=> api.post('/reactions', {article_id:a.id, value:-1}).then(()=> window.location.reload())}>👎 {a.dislikes}</button>
        <button className="btn btn-outline-secondary" onClick={()=> api.post('/bookmarks/toggle', {article_id:a.id}).then(()=> alert('Добавлено/удалено из закладок'))}>★ В закладки</button>
      </div>

      <hr className="my-4"/>

      <div className="d-flex align-items-center gap-3">
        <div>
          <strong>Рейтинг:</strong>
          <span className="badge text-bg-info ms-2">{(a.rating_avg||0).toFixed(1)}/5</span>
          <span className="text-muted small ms-1">({a.rating_count})</span>
        </div>
        <div className="d-inline-flex align-items-center gap-2">
          <select id="score" className="form-select form-select-sm" defaultValue={5} style={{width:'auto'}}>
            {[1,2,3,4,5].map(n=> <option key={n} value={n}>{n}</option>)}
          </select>
          <button className="btn btn-sm btn-primary" onClick={()=> {
            const score = Number(document.getElementById('score').value)
            api.post('/ratings', {article_id:a.id, score}).then(()=> window.location.reload())
          }}>Оценить</button>
        </div>
      </div>
    </div>
  )
}


