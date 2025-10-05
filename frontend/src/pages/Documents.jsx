import React, { useState, useEffect } from 'react'
import { documentService } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const Documents = () => {
  const { user } = useAuth()
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    document_type: ''
  })

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const data = await documentService.getAll()
      setDocuments(data)
    } catch (error) {
      console.error('Error loading documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await documentService.create(formData)
      setFormData({ title: '', description: '', document_type: '' })
      setShowForm(false)
      loadDocuments()
    } catch (error) {
      console.error('Error creating document:', error)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este documento?')) {
      try {
        await documentService.delete(id)
        loadDocuments()
      } catch (error) {
        console.error('Error deleting document:', error)
      }
    }
  }

  const handleSign = async (id) => {
    const signature = prompt('Ingrese su firma digital:')
    if (signature) {
      try {
        await documentService.sign(id, signature)
        loadDocuments()
        alert('Documento firmado exitosamente')
      } catch (error) {
        console.error('Error signing document:', error)
        alert('Error al firmar el documento')
      }
    }
  }

  if (loading) {
    return <div className="loading">Cargando...</div>
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Documentos</h2>
        <button className="button" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : 'Nuevo Documento'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Nuevo Documento</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Título</label>
              <input
                type="text"
                className="input"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Tipo de Documento</label>
              <select
                className="input"
                value={formData.document_type}
                onChange={(e) => setFormData({ ...formData, document_type: e.target.value })}
                required
              >
                <option value="">Seleccione...</option>
                <option value="Contrato">Contrato</option>
                <option value="Certificado">Certificado</option>
                <option value="Memorando">Memorando</option>
                <option value="Informe">Informe</option>
                <option value="Otro">Otro</option>
              </select>
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
            <button type="submit" className="button">Crear Documento</button>
          </form>
        </div>
      )}

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Título</th>
              <th>Tipo</th>
              <th>Estado</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id}>
                <td>{doc.id}</td>
                <td>{doc.title}</td>
                <td>{doc.document_type}</td>
                <td>
                  {doc.is_signed ? (
                    <span style={{ color: 'green' }}>✓ Firmado</span>
                  ) : (
                    <span style={{ color: 'orange' }}>Pendiente</span>
                  )}
                </td>
                <td>{new Date(doc.created_at).toLocaleDateString()}</td>
                <td>
                  {!doc.is_signed && doc.user_id === user?.id && (
                    <button
                      className="button"
                      onClick={() => handleSign(doc.id)}
                      style={{ marginRight: '5px', fontSize: '12px', padding: '5px 10px' }}
                    >
                      Firmar
                    </button>
                  )}
                  {(doc.user_id === user?.id || ['TI', 'Administración'].includes(user?.role)) && (
                    <button
                      className="button button-danger"
                      onClick={() => handleDelete(doc.id)}
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
        {documents.length === 0 && (
          <p style={{ textAlign: 'center', padding: '20px', color: '#6c757d' }}>
            No hay documentos disponibles
          </p>
        )}
      </div>
    </div>
  )
}

export default Documents
