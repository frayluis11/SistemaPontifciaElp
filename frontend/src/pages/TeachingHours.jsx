import React, { useState, useEffect } from 'react'
import { teachingHourService } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const TeachingHours = () => {
  const { user } = useAuth()
  const [hours, setHours] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    subject: '',
    course: '',
    hours: '',
    date: '',
    description: ''
  })

  useEffect(() => {
    loadHours()
  }, [])

  const loadHours = async () => {
    try {
      const data = await teachingHourService.getAll()
      setHours(data)
    } catch (error) {
      console.error('Error loading teaching hours:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await teachingHourService.create(formData)
      setFormData({ subject: '', course: '', hours: '', date: '', description: '' })
      setShowForm(false)
      loadHours()
    } catch (error) {
      console.error('Error creating teaching hour:', error)
      alert('Error al crear registro de horas')
    }
  }

  const handleApprove = async (id) => {
    try {
      await teachingHourService.approve(id)
      loadHours()
      alert('Horas aprobadas exitosamente')
    } catch (error) {
      console.error('Error approving hours:', error)
      alert('Error al aprobar horas')
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este registro?')) {
      try {
        await teachingHourService.delete(id)
        loadHours()
      } catch (error) {
        console.error('Error deleting teaching hour:', error)
      }
    }
  }

  if (loading) {
    return <div className="loading">Cargando...</div>
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Horas Docentes</h2>
        {user?.role === 'Docente' && (
          <button className="button" onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancelar' : 'Registrar Horas'}
          </button>
        )}
      </div>

      {showForm && user?.role === 'Docente' && (
        <div className="card">
          <h3>Registrar Horas Docentes</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Materia</label>
              <input
                type="text"
                className="input"
                value={formData.subject}
                onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Curso</label>
              <input
                type="text"
                className="input"
                value={formData.course}
                onChange={(e) => setFormData({ ...formData, course: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Horas</label>
              <input
                type="number"
                step="0.5"
                className="input"
                value={formData.hours}
                onChange={(e) => setFormData({ ...formData, hours: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Fecha</label>
              <input
                type="datetime-local"
                className="input"
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea
                className="input"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows="3"
              />
            </div>
            <button type="submit" className="button">Registrar</button>
          </form>
        </div>
      )}

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Materia</th>
              <th>Curso</th>
              <th>Horas</th>
              <th>Fecha</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {hours.map((hour) => (
              <tr key={hour.id}>
                <td>{hour.id}</td>
                <td>{hour.subject}</td>
                <td>{hour.course}</td>
                <td>{hour.hours}h</td>
                <td>{new Date(hour.date).toLocaleDateString()}</td>
                <td>
                  {hour.is_approved ? (
                    <span style={{ color: 'green' }}>✓ Aprobado</span>
                  ) : (
                    <span style={{ color: 'orange' }}>Pendiente</span>
                  )}
                </td>
                <td>
                  {!hour.is_approved && ['RRHH', 'Administración', 'TI'].includes(user?.role) && (
                    <button
                      className="button"
                      onClick={() => handleApprove(hour.id)}
                      style={{ marginRight: '5px', fontSize: '12px', padding: '5px 10px' }}
                    >
                      Aprobar
                    </button>
                  )}
                  {(hour.teacher_id === user?.id || ['TI', 'Administración'].includes(user?.role)) && (
                    <button
                      className="button button-danger"
                      onClick={() => handleDelete(hour.id)}
                      style={{ fontSize: '12px', padding: '5px 10px' }}
                    >
                      Eliminar
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {hours.length === 0 && (
          <p style={{ textAlign: 'center', padding: '20px', color: '#6c757d' }}>
            No hay registros de horas disponibles
          </p>
        )}
      </div>
    </div>
  )
}

export default TeachingHours
