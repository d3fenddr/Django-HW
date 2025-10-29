import { Link, Routes, Route, Navigate } from 'react-router-dom'
import ArticlesPage from './pages/ArticlesPage.jsx'
import PopularPage from './pages/PopularPage.jsx'
import CategoriesPage from './pages/CategoriesPage.jsx'
import AuthorsPage from './pages/AuthorsPage.jsx'
import AuthorDetailPage from './pages/AuthorDetailPage.jsx'
import ArticleDetailPage from './pages/ArticleDetailPage.jsx'
import BookmarksPage from './pages/BookmarksPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import SignupPage from './pages/SignupPage.jsx'

export default function App() {
  return (
    <div>
      <nav className="navbar navbar-expand-lg bg-body-tertiary mb-4">
        <div className="container">
          <Link className="navbar-brand" to="/">Habr Lite</Link>
          <div className="d-flex gap-2">
            <Link className="btn btn-link" to="/">Статьи</Link>
            <Link className="btn btn-link" to="/popular">Популярное</Link>
            <Link className="btn btn-link" to="/categories">Категории</Link>
            <Link className="btn btn-link" to="/authors">Авторы</Link>
          </div>
          <div className="ms-auto d-flex gap-2 align-items-center">
            <Link className="btn btn-outline-secondary btn-sm" to="/bookmarks">Закладки</Link>
            <Link className="btn btn-outline-secondary btn-sm" to="/login">Войти</Link>
            <Link className="btn btn-primary btn-sm" to="/signup">Регистрация</Link>
          </div>
        </div>
      </nav>
      <main className="container">
        <Routes>
          <Route index element={<ArticlesPage/>} />
          <Route path="popular" element={<PopularPage/>} />
          <Route path="categories" element={<CategoriesPage/>} />
          <Route path="authors" element={<AuthorsPage/>} />
          <Route path="authors/:id" element={<AuthorDetailPage/>} />
          <Route path="articles/:slug" element={<ArticleDetailPage/>} />
          <Route path="bookmarks" element={<BookmarksPage/>} />
          <Route path="login" element={<LoginPage/>} />
          <Route path="signup" element={<SignupPage/>} />
          <Route path="*" element={<Navigate to="/" replace/>} />
        </Routes>
      </main>
    </div>
  )
}


