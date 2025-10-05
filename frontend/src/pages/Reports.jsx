import React, { useState, useEffect } from 'react'
import { reportService } from '../services/api'

const Reports = () => {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadReports()
  }, [])

  const loadReports = async () => {
    try {
      const data = await reportService.getAll()
      setReports(data)
    } catch (error) {
      console.error('Error loading reports:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleExportDocuments = async () => {
    try {
      const blob = await reportService.exportDocuments()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'documentos.xlsx'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exporting documents:', error)
      alert('Error al exportar documentos')
    }
  }

  const handleExportTeachingHours = async () => {
    try {
      const blob = await reportService.exportTeachingHours()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'horas_docentes.xlsx'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exporting teaching hours:', error)
      alert('Error al exportar horas docentes')
    }
  }

  if (loading) {
    return <div className="loading">Cargando...</div>
  }

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>Reportes y Exportación</h2>

      <div className="card">
        <h3>Exportar Datos</h3>
        <p style={{ marginBottom: '20px', color: '#6c757d' }}>
          Exporte los datos del sistema a archivos Excel para análisis o archivo.
        </p>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="button" onClick={handleExportDocuments}>
            📄 Exportar Documentos
          </button>
          <button className="button" onClick={handleExportTeachingHours}>
            📊 Exportar Horas Docentes
          </button>
        </div>
      </div>

      <div className="card">
        <h3>Reportes Generados</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Título</th>
              <th>Tipo</th>
              <th>Fecha de Creación</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => (
              <tr key={report.id}>
                <td>{report.id}</td>
                <td>{report.title}</td>
                <td>{report.report_type}</td>
                <td>{new Date(report.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {reports.length === 0 && (
          <p style={{ textAlign: 'center', padding: '20px', color: '#6c757d' }}>
            No hay reportes disponibles
          </p>
        )}
      </div>

      <div className="card">
        <h3>Estadísticas del Sistema</h3>
        <p style={{ color: '#6c757d' }}>
          Las estadísticas detalladas están disponibles en el Dashboard.
        </p>
      </div>
    </div>
  )
}

export default Reports
