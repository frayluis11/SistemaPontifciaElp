import React from 'react'
import { Outlet, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const Layout = () => {
  const { user, logout } = useAuth()

  return (
    <div>
      <nav className="navbar">
        <div>
          <h1>Sistema Pontificia ELP</h1>
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <span style={{ marginRight: '20px' }}>
            {user?.full_name || user?.username} ({user?.role})
          </span>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/documents">Documentos</Link>
          {user?.role === 'Docente' && (
            <Link to="/teaching-hours">Horas Docentes</Link>
          )}
          {['RRHH', 'Contabilidad', 'Administración', 'TI'].includes(user?.role) && (
            <>
              <Link to="/teaching-hours">Horas Docentes</Link>
              <Link to="/reports">Reportes</Link>
            </>
          )}
          <button className="button button-secondary" onClick={logout} style={{ marginLeft: '10px' }}>
            Cerrar Sesión
          </button>
        </div>
      </nav>
      <div className="container">
        <Outlet />
      </div>
    </div>
  )
}

export default Layout
