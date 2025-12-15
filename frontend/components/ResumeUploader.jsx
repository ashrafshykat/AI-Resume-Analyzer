import React, { useState } from 'react'
import axios from 'axios'
import styles from './ResumeUploader.module.css'

export default function ResumeUploader() {
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [uploadMode, setUploadMode] = useState('file') // 'file' or 'text'

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile)
      setError('')
    } else {
      setError('Please select a valid PDF file')
      setFile(null)
    }
  }

  const handleTextChange = (e) => {
    setText(e.target.value)
    setError('')
  }

  const handleAnalyze = async () => {
    setError('')
    setResult(null)

    if (uploadMode === 'file' && !file) {
      setError('Please select a PDF file')
      return
    }

    if (uploadMode === 'text' && !text.trim()) {
      setError('Please enter resume text')
      return
    }

    setLoading(true)

    try {
      const formData = new FormData()
      if (uploadMode === 'file') {
        formData.append('file', file)
      } else {
        formData.append('text', text)
      }

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/analyze`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      )

      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error analyzing resume. Please try again.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>AI Resume Analyzer</h1>
        <p className={styles.subtitle}>Upload or paste your resume for instant analysis</p>

        <div className={styles.modeToggle}>
          <button
            className={`${styles.modeBtn} ${uploadMode === 'file' ? styles.active : ''}`}
            onClick={() => {
              setUploadMode('file')
              setText('')
              setFile(null)
              setError('')
            }}
          >
            📁 PDF Upload
          </button>
          <button
            className={`${styles.modeBtn} ${uploadMode === 'text' ? styles.active : ''}`}
            onClick={() => {
              setUploadMode('text')
              setFile(null)
              setError('')
            }}
          >
            📝 Paste Text
          </button>
        </div>

        {uploadMode === 'file' ? (
          <div className={styles.uploadArea}>
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              id="fileInput"
              style={{ display: 'none' }}
            />
            <label htmlFor="fileInput" className={styles.uploadLabel}>
              <div className={styles.uploadContent}>
                <div className={styles.uploadIcon}>📤</div>
                <p>Click the button to select a PDF file</p>
                {file && <p className={styles.fileName}>✓ {file.name}</p>}
              </div>
            </label>
          </div>
        ) : (
          <textarea
            className={styles.textArea}
            placeholder="Paste your resume text here..."
            value={text}
            onChange={handleTextChange}
            rows={8}
          />
        )}

        {error && <div className={styles.error}>❌ {error}</div>}

        <button
          className={styles.analyzeBtn}
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? '⏳ Analyzing...' : '🔍 Analyze Resume'}
        </button>

        {/* Results */}
        {result && (
          <div className={styles.results}>
            <h2>✅ Analysis Results</h2>

            {/* Candidate Info */}
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>👤 Candidate Information</h3>
              <div className={styles.infoGrid}>
                <div className={styles.infoItem}>
                  <span className={styles.label}>Name:</span>
                  <span className={styles.value}>{result.name || 'N/A'}</span>
                </div>
                <div className={styles.infoItem}>
                  <span className={styles.label}>Email:</span>
                  <span className={styles.value}>{result.email || 'N/A'}</span>
                </div>
                <div className={styles.infoItem}>
                  <span className={styles.label}>Phone:</span>
                  <span className={styles.value}>{result.phone || 'N/A'}</span>
                </div>
              </div>
            </div>

            {/* Experience */}
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>💼 Experience</h3>
              <div className={styles.infoGrid}>
                <div className={styles.infoItem}>
                  <span className={styles.label}>Total Years:</span>
                  <span className={styles.value}>{result.experience_years} years</span>
                </div>
                <div className={styles.infoItem}>
                  <span className={styles.label}>Level:</span>
                  <span className={`${styles.value} ${styles[result.experience_level.toLowerCase()]}`}>
                    {result.experience_level}
                  </span>
                </div>
              </div>
            </div>

            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>🎯 Job Role Classification</h3>
              <div className={styles.classificationBox}>
                <div className={styles.classification}>{result.classification}</div>
                <div className={styles.confidence}>
                  Confidence: <span className={styles.confidenceValue}>{(result.confidence * 100).toFixed(1)}%</span>
                </div>
              </div>
              <div className={styles.confidenceBar}>
                <div
                  className={styles.confidenceBarFill}
                  style={{ width: `${result.confidence * 100}%` }}
                />
              </div>
            </div>

            {result.skills.length > 0 && (
              <div className={styles.section}>
                <h3 className={styles.sectionTitle}>🔧 Detected Skills</h3>
                <div className={styles.skills}>
                  {result.skills.map((skill, idx) => (
                    <span key={idx} className={styles.skill}>
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {result.education.length > 0 && (
              <div className={styles.section}>
                <h3 className={styles.sectionTitle}>🎓 Education</h3>
                <ul className={styles.educationList}>
                  {result.education.map((edu, idx) => (
                    <li key={idx}>{edu}</li>
                  ))}
                </ul>
              </div>
            )}

            <button
              className={styles.resetBtn}
              onClick={() => {
                setResult(null)
                setFile(null)
                setText('')
              }}
            >
              ↺ Analyze Another Resume
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
