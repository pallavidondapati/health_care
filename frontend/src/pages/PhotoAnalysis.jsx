import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Camera, Upload, AlertTriangle, CheckCircle, Activity } from "lucide-react";
import axios from "axios";

const API = "http://127.0.0.1:8000/api";

const SEVERITY_CONFIG = {
  mild:     { color: "#16a34a", bg: "#f0fdf4", label: "Mild" },
  moderate: { color: "#d97706", bg: "#fffbeb", label: "Moderate" },
  severe:   { color: "#dc2626", bg: "#fef2f2", label: "Severe" },
};

export default function PhotoAnalysis() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileRef = useRef(null);
  const cameraRef = useRef(null);
  const navigate = useNavigate();

  const handleFile = (file) => {
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
    setError(null);
  };

  const analyzePhoto = async () => {
    if (!image) return;
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("image", image);
      const res = await axios.post(`${API}/analyze-photo`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not analyze image");
    } finally {
      setLoading(false);
    }
  };

  const sev = result?.severity_hint ? SEVERITY_CONFIG[result.severity_hint] : null;

  return (
    <div style={styles.container}>
      <div style={styles.blob1} />

      {/* Header */}
      <div style={styles.topBar}>
        <button onClick={() => navigate("/")} style={styles.backBtn}>
          <ArrowLeft size={16} /> Back
        </button>
        <h2 style={styles.title}>Symptom Photo</h2>
        <div style={{ width: 60 }} />
      </div>

      <div style={styles.content}>
        <p style={styles.subtitle}>
          Take or upload a photo of your skin, wound, rash, or any visible symptom
        </p>

        {/* Upload Buttons */}
        {!preview && (
          <div style={styles.uploadArea}>
            <div style={styles.uploadIcon}>📸</div>
            <p style={styles.uploadTitle}>Upload or take a photo</p>
            <p style={styles.uploadHint}>Skin rash, wound, eye redness, swelling...</p>

            <div style={styles.btnRow}>
              {/* Camera */}
              <label style={styles.cameraBtn}>
                <Camera size={18} />
                Take Photo
                <input
                  ref={cameraRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  style={{ display: "none" }}
                  onChange={e => handleFile(e.target.files[0])}
                />
              </label>

              {/* Upload */}
              <label style={styles.uploadBtn}>
                <Upload size={18} />
                Upload
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  style={{ display: "none" }}
                  onChange={e => handleFile(e.target.files[0])}
                />
              </label>
            </div>
          </div>
        )}

        {/* Preview */}
        {preview && (
          <div style={styles.previewContainer}>
            <img src={preview} alt="symptom" style={styles.previewImage} />
            <div style={styles.previewBtns}>
              <button
                onClick={() => { setImage(null); setPreview(null); setResult(null); }}
                style={styles.retakeBtn}
              >
                Retake
              </button>
              {!result && (
                <button
                  onClick={analyzePhoto}
                  disabled={loading}
                  style={styles.analyzeBtn}
                >
                  {loading ? "Analyzing..." : "🔍 Analyze"}
                </button>
              )}
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div style={styles.loadingBox}>
            <div style={styles.spinner} />
            <p style={styles.loadingText}>Analyzing your photo with AI...</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div style={styles.errorBox}>
            <p style={{ color: "#dc2626", fontSize: 13 }}>⚠️ {error}</p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div style={styles.results}>

            {/* Emergency Banner */}
            {result.is_emergency && (
              <div style={styles.emergencyBanner}>
                <AlertTriangle size={20} color="white" />
                <div>
                  <p style={styles.emergencyTitle}>Seek immediate medical help!</p>
                  <a href="tel:108" style={styles.call108}>Call 108 →</a>
                </div>
              </div>
            )}

            {/* Severity */}
            {sev && (
              <div style={{ ...styles.severityCard, background: sev.bg, border: `1px solid ${sev.color}30` }}>
                <Activity size={18} color={sev.color} />
                <span style={{ color: sev.color, fontWeight: 700, fontSize: 15 }}>
                  {sev.label} — {result.description}
                </span>
              </div>
            )}

            {/* Symptoms Detected */}
            {result.symptoms_detected?.length > 0 && (
              <div style={styles.card}>
                <h4 style={styles.cardTitle}>🔍 Detected</h4>
                <div style={styles.tagRow}>
                  {result.symptoms_detected.map((s, i) => (
                    <span key={i} style={styles.tag}>{s}</span>
                  ))}
                </div>
              </div>
            )}

            {/* Advice */}
            {result.advice && (
              <div style={styles.card}>
                <h4 style={styles.cardTitle}>💊 Immediate Advice</h4>
                <p style={styles.cardText}>{result.advice}</p>
              </div>
            )}

            {/* What NOT to do */}
            {result.what_not_to_do && (
              <div style={{ ...styles.card, border: "1px solid #fecaca", background: "#fef2f2" }}>
                <h4 style={{ ...styles.cardTitle, color: "#dc2626" }}>⚠️ Do NOT</h4>
                <p style={styles.cardText}>{result.what_not_to_do}</p>
              </div>
            )}

            {/* Visit Doctor */}
            {result.visit_doctor && (
              <div style={{ ...styles.card, border: "1px solid #bbf7d0", background: "#f0fdf4" }}>
                <CheckCircle size={16} color="#16a34a" />
                <p style={{ ...styles.cardText, color: "#15803d", fontWeight: 500 }}>
                  Please visit a doctor or PHC for proper examination and treatment.
                </p>
              </div>
            )}

            {/* Analyze Voice */}
            <button
              onClick={() => navigate("/")}
              style={styles.voiceBtn}
            >
              🎙️ Also describe symptoms by voice →
            </button>
          </div>
        )}
      </div>

      <p style={styles.disclaimer}>
        VaaniCare photo analysis is for guidance only. Always consult a doctor.
      </p>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh", display: "flex", flexDirection: "column",
    alignItems: "center", maxWidth: 480,
    margin: "0 auto", position: "relative", background: "#f0fdf4",
  },
  blob1: {
    position: "fixed", top: -100, right: -100, width: 300, height: 300,
    borderRadius: "50%",
    background: "radial-gradient(circle, #bbf7d0 0%, transparent 70%)",
    zIndex: 0, pointerEvents: "none",
  },
  topBar: {
    width: "100%", display: "flex", alignItems: "center",
    justifyContent: "space-between", padding: "16px 20px",
    background: "white", boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
  },
  backBtn: {
    display: "flex", alignItems: "center", gap: 4,
    background: "none", border: "none", cursor: "pointer",
    color: "#6b7280", fontSize: 13, fontFamily: "Sora, sans-serif",
  },
  title: { fontSize: 17, fontWeight: 700, color: "#14532d" },
  content: {
    width: "100%", padding: "20px 16px",
    display: "flex", flexDirection: "column", gap: 14, zIndex: 1,
  },
  subtitle: { fontSize: 14, color: "#6b7280", textAlign: "center" },
  uploadArea: {
    background: "white", borderRadius: 24,
    padding: "36px 24px", display: "flex",
    flexDirection: "column", alignItems: "center",
    boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
    border: "2px dashed #bbf7d0",
  },
  uploadIcon: { fontSize: 48, marginBottom: 12 },
  uploadTitle: { fontSize: 16, fontWeight: 600, color: "#1f2937", marginBottom: 6 },
  uploadHint: { fontSize: 13, color: "#9ca3af", marginBottom: 24, textAlign: "center" },
  btnRow: { display: "flex", gap: 12 },
  cameraBtn: {
    display: "flex", alignItems: "center", gap: 8,
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    color: "white", padding: "12px 20px", borderRadius: 14,
    fontSize: 14, fontWeight: 600, cursor: "pointer",
  },
  uploadBtn: {
    display: "flex", alignItems: "center", gap: 8,
    background: "white", color: "#16a34a",
    border: "1.5px solid #16a34a",
    padding: "12px 20px", borderRadius: 14,
    fontSize: 14, fontWeight: 600, cursor: "pointer",
  },
  previewContainer: {
    display: "flex", flexDirection: "column", gap: 12,
  },
  previewImage: {
    width: "100%", borderRadius: 20,
    maxHeight: 300, objectFit: "cover",
    boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
  },
  previewBtns: { display: "flex", gap: 10 },
  retakeBtn: {
    flex: 1, padding: "12px", borderRadius: 14,
    border: "1.5px solid #e5e7eb", background: "white",
    color: "#6b7280", fontSize: 14, fontWeight: 600, cursor: "pointer",
  },
  analyzeBtn: {
    flex: 2, padding: "12px", borderRadius: 14, border: "none",
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    color: "white", fontSize: 14, fontWeight: 600, cursor: "pointer",
  },
  loadingBox: {
    display: "flex", flexDirection: "column",
    alignItems: "center", gap: 12, padding: 24,
  },
  spinner: {
    width: 36, height: 36, border: "3px solid #e5e7eb",
    borderTop: "3px solid #16a34a", borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  loadingText: { color: "#6b7280", fontSize: 14 },
  errorBox: {
    background: "#fef2f2", border: "1px solid #fecaca",
    borderRadius: 12, padding: "12px 16px",
  },
  results: { display: "flex", flexDirection: "column", gap: 12 },
  emergencyBanner: {
    background: "linear-gradient(135deg, #dc2626, #991b1b)",
    borderRadius: 16, padding: "16px 20px",
    display: "flex", alignItems: "center", gap: 12,
    boxShadow: "0 4px 16px rgba(220,38,38,0.3)",
  },
  emergencyTitle: { color: "white", fontWeight: 700, fontSize: 15 },
  call108: {
    color: "white", fontSize: 13,
    textDecoration: "underline", display: "block", marginTop: 4,
  },
  severityCard: {
    borderRadius: 14, padding: "14px 16px",
    display: "flex", alignItems: "center", gap: 10,
  },
  card: {
    background: "white", borderRadius: 16, padding: "16px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
    display: "flex", flexDirection: "column", gap: 8,
  },
  cardTitle: { fontSize: 14, fontWeight: 700, color: "#1f2937" },
  cardText: { fontSize: 14, color: "#374151", lineHeight: 1.6 },
  tagRow: { display: "flex", flexWrap: "wrap", gap: 8 },
  tag: {
    background: "#eff6ff", color: "#1d4ed8",
    padding: "4px 12px", borderRadius: 20,
    fontSize: 13, fontWeight: 500, textTransform: "capitalize",
  },
  voiceBtn: {
    padding: "14px", borderRadius: 16, border: "none",
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    color: "white", fontSize: 14, fontWeight: 600,
    cursor: "pointer", textAlign: "center",
  },
  disclaimer: {
    fontSize: 11, color: "#9ca3af",
    textAlign: "center", padding: "12px 32px 24px",
  },
};