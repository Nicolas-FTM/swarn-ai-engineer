import { useState } from 'react'
import './DocumentUpload.css'
import { apiClient } from '../services/api'

function DocumentUpload() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [documents, setDocuments] = useState([])

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await apiClient.post('/api/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      setDocuments([...documents, response.data])
      setFile(null)
      alert('Document uploaded successfully')
    } catch (error) {
      console.error('Error uploading document:', error)
      alert('Error uploading document')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="document-upload">
      <h3>Upload Documents</h3>
      
      <form onSubmit={handleUpload}>
        <input
          type="file"
          onChange={handleFileChange}
          disabled={uploading}
          accept=".pdf,.txt,.docx"
        />
        <button type="submit" disabled={!file || uploading}>
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>

      {documents.length > 0 && (
        <div className="documents-list">
          <h4>Documents</h4>
          <ul>
            {documents.map((doc) => (
              <li key={doc.id}>
                {doc.filename} ({doc.status})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default DocumentUpload
