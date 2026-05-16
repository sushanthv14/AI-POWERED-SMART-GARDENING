import React, { useState } from 'react';
import '../styles/PredictPage.css';
import { predictDisease } from '../services/plantService';
import { PredictionResponse } from '../types';

const PredictPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(selectedFile);
      setError(null);
      setResult(null);
    }
  };

  const handlePredictClick = async () => {
    if (!file) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictDisease(file);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="predict-container">
      <div className="predict-card">
        <h2>Plant Disease Prediction</h2>
        <p className="subtitle">Upload an image of your plant to analyze for diseases</p>

        <div className="upload-section">
          {!preview ? (
            <label className="upload-label">
              <div className="upload-box">
                <span className="upload-icon">📸</span>
                <p>Click to upload image</p>
                <p className="upload-hint">or drag and drop</p>
              </div>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
            </label>
          ) : (
            <div className="preview-section">
              <img src={preview} alt="Preview" className="preview-image" />
              <p className="file-name">{file?.name}</p>
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        {result && (
          <div className="result-section">
            <h3>Prediction Result</h3>
            <div className="result-item">
              <label>Plant:</label>
              <span className="result-value">{result.plant_name}</span>
            </div>
            <div className="result-item">
              <label>Disease:</label>
              <span className="result-value">{result.disease_name}</span>
            </div>
            <div className="result-item">
              <label>Confidence:</label>
              <span className="result-value">{(result.disease_confidence * 100).toFixed(2)}%</span>
            </div>
            <div className="result-item">
              <label>Summary:</label>
              <span className="result-value">{result.summary}</span>
            </div>
            <div className="result-item">
              <label>Next step:</label>
              <span className="result-value">{result.recommended_next_step}</span>
            </div>
          </div>
        )}

        <div className="button-group">
          <button
            onClick={handlePredictClick}
            disabled={!file || loading}
            className="predict-button"
          >
            {loading ? 'Analyzing...' : 'Predict Disease'}
          </button>
          {(file || result) && (
            <button onClick={handleClear} className="clear-button">
              Clear
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PredictPage;
