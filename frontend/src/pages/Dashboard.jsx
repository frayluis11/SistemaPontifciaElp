import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { documentService, teachingHourService } from '../services/api'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    documents: 0,
    signedDocuments: 0,
    teachingHours: 0,
    approvedHours: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const documents = await documentService.getAll()
      const signedDocs = documents.filter(d => d.is_signed)
      
      let hours = []
      let approvedHours = []
      
      if (user?.role === 'Docente' || ['RRHH', 'Contabilidad', 'Administración', 'TI'].includes(user?.role)) {
        hours = await teachingHourService.getAll()
        approvedHours = hours.filter(h => h.is_approved)
      }

      setStats({
        documents: documents.length,
        signedDocuments: signedDocs.length,
        teachingHours: hours.length,
        approvedHours: approvedHours.length
      })
    } catch (error) {
      console.error('Error loading stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Cargando...</div>
  }

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>Dashboard - {user?.role}</h2>
      
      <div className="dashboard-grid">
        <div className="stat-card">
          <h3>Documentos Totales</h3>
          <div className="value">{stats.documents}</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
          <h3>Documentos Firmados</h3>
          <div className="value">{stats.signedDocuments}</div>
        </div>
        
        {(user?.role === 'Docente' || ['RRHH', 'Contabilidad', 'Administración', 'TI'].includes(user?.role)) && (
          <>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
              <h3>Horas Docentes</h3>
              <div className="value">{stats.teachingHours}</div>
            </div>
            
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}>
              <h3>Horas Aprobadas</h3>
              <div className="value">{stats.approvedHours}</div>
            </div>
          </>
        )}
      </div>

      <div className="card" style={{ marginTop: '30px' }}>
        <h3>Bienvenido al Sistema Pontificia ELP</h3>
        <p style={{ marginTop: '10px', lineHeight: '1.6' }}>
          Este sistema permite gestionar documentos laborales, horas docentes y reportes digitales
          de manera eficiente y segura.
        </p>
        <div style={{ marginTop: '20px' }}>
          <h4>Funcionalidades según tu rol ({user?.role}):</h4>
          <ul style={{ marginTop: '10px', paddingLeft: '20px' }}>
            <li>Gestión de documentos laborales</li>
            <li>Firma digital de documentos</li>
            {user?.role === 'Docente' && (
              <>
                <li>Registro de horas docentes</li>
                <li>Seguimiento de horas aprobadas</li>
              </>
            )}
            {['RRHH', 'Contabilidad', 'Administración', 'TI'].includes(user?.role) && (
              <>
                <li>Aprobación de horas docentes</li>
                <li>Generación de reportes</li>
                <li>Exportación de datos a Excel</li>
              </>
            )}
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
