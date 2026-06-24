import { useState } from 'react';
import styles from "./DocumentUpload.module.css";
import { apiClient } from '../../services/api';

interface Document {
  id: string
  filename: string
  status: string
}

function DocumentUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState<boolean>(false)
  const [documents, setDocuments] = useState<Document[]>([])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (!file) return

    setUploading(true)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await apiClient.post('/api/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      setDocuments(prev => [...prev, response.data])
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
    <div className={styles["document-upload"]}>
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
        <div className={styles["documents-list"]}>
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