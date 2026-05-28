import React, { useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  AlertTriangle, CheckCircle, Phone, MapPin,
  Volume2, ArrowLeft, Activity, Mic, ShieldCheck
} from 'lucide-react';
import axios from 'axios';

const API = "http://127.0.0.1:8000/api";

const SEVERITY_CONFIG = {
  low: {
    label: "Low Risk",
    emoji: "🟢",
    gradient: "linear-gradient(135deg, #16a34a, #15803d)",
    bg: "#f0fdf4",
    border: "#bbf7d0",
    badge: { background: "#dcfce7", color: "#15803d" },
    icon: <CheckCircle size={20} color="#16a34a" />,
  },
  moderate: {
    label: "Moderate",
    emoji: "🟡",
    gradient: "linear-gradient(135deg, #d97706, #ca8a04)",
    bg: "#fffbeb",
    border: "#fde68a",
    badge: { background: "#fef3c7", color: "#92400e" },
    icon: <Activity size={20} color="#d97706" />,
  },
  high: {
    label: "High Risk",
    emoji: "🟠",
    gradient: "linear-gradient(135deg, #ea580c, #dc2626)",
    bg: "#fff7ed",
    border: "#fed7aa",
    badge: { background: "#ffedd5", color: "#9a3412" },
    icon: <AlertTriangle size={20} color="#ea580c" />,
  },
  emergency: {
    label: "Emergency",
    emoji: "🔴",
    gradient: "linear-gradient(135deg, #dc2626, #991b1b)",
    bg: "#fef2f2",
    border: "#fecaca",
    badge: { background: "#fee2e2", color: "#991b1b" },
    icon: <AlertTriangle size={20} color="#dc2626" />,
  },
};

export default function Result() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const audioRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const data = state?.data;

  if (!data) { navigate("/"); return null; }

  const sev = SEVERITY_CONFIG[data.severity] || SEVERITY_CONFIG.moderate;

 const playResponse = async () => {
    try {
        setPlaying(true);
        const res = await axios.post(
            `${API}/text-to-speech`,
            { text: data.response, language: data.language },
            { responseType: "blob" }  // ✅ must be blob
        );
        const blob = new Blob([res.data], { type: "audio/mpeg" });  // ✅ explicit type
        const url = URL.createObjectURL(blob);
        if (audioRef.current) {
            audioRef.current.src = url;
            audioRef.current.load();     // ✅ force reload
            audioRef.current.play();
            audioRef.current.onended = () => setPlaying(false);
        }
    } catch (err) {
        setPlaying(false);
        console.error("TTS error:", err);
        alert("Could not play audio. Check internet connection.");
    }
};

  return (
    <div style={styles.container}>
      <div style={styles.blob1} />
      <div style={styles.blob2} />

      {/* Top Bar */}
      <div style={styles.topBar}>
        <button onClick={() => navigate("/")} style={styles.backBtn}>
          <ArrowLeft size={16} /> Back
        </button>
        <div style={styles.logoSmall}>
          <span style={styles.logoSmallText}>VaaniCare</span>
        </div>
        <button onClick={() => navigate("/")} style={styles.newBtn}>
          <Mic size={14} /> New
        </button>
      </div>

      {/* Emergency Banner */}
      {data.call_108 && (
        <div style={styles.emergencyBanner} className="animate-fadeUp">
          <div>
            <p style={styles.emergencyTitle}>🚨 Medical Emergency!</p>
            <p style={styles.emergencySubtitle}>Seek immediate medical help</p>
          </div>
          <a href="tel:108" style={styles.callBtn}>
            <Phone size={16} /> Call 108
          </a>
        </div>
      )}

      {/* Severity Header Card */}
      <div style={{ ...styles.severityCard, background: sev.gradient }} className="animate-fadeUp">
        <div style={styles.severityTop}>
          <span style={{ ...styles.severityBadge, ...sev.badge }}>
            {sev.emoji} {sev.label}
          </span>
          <span style={styles.confidenceText}>
            {Math.round((data.debug?.triage_confidence || 0) * 100)}% confidence
          </span>
        </div>
        <p style={styles.transcriptLabel}>You said:</p>
        <p style={styles.transcriptText}>"{data.transcript}"</p>
        <div style={styles.langBadge}>
          🌐 {data.language?.toUpperCase()}
        </div>
      </div>

      {/* Symptoms */}
      {data.symptoms?.length > 0 && (
        <div style={styles.card} className="animate-fadeUp">
          <div style={styles.cardHeader}>
            <ShieldCheck size={18} color="#16a34a" />
            <h3 style={styles.cardTitle}>Detected Symptoms</h3>
          </div>
          <div style={styles.symptomRow}>
            {data.symptoms.map((s, i) => (
              <span key={i} style={styles.symptomTag}>{s}</span>
            ))}
          </div>
          {data.duration && (
            <p style={styles.durationText}>⏱ Duration: {data.duration}</p>
          )}
        </div>
      )}

      {/* AI Response */}
      <div style={styles.card} className="animate-fadeUp">
        <div style={styles.cardHeader}>
          <Activity size={18} color="#0d9488" />
          <h3 style={styles.cardTitle}>Health Guidance</h3>
          <button onClick={playResponse} style={styles.listenBtn} disabled={playing}>
            <Volume2 size={14} />
            {playing ? "Playing..." : "Listen"}
          </button>
        </div>
        <p style={styles.responseText}>{data.response}</p>
        <audio ref={audioRef} style={{ display: "none" }} />
      </div>

      {/* Nearby Facilities */}
      {data.facilities?.length > 0 && (
        <div style={styles.card} className="animate-fadeUp">
          <div style={styles.cardHeader}>
            <MapPin size={18} color="#dc2626" />
            <h3 style={styles.cardTitle}>Nearby Facilities</h3>
          </div>
          <div style={styles.facilityList}>
            {data.facilities.map((f, i) => (
              <div key={i} style={styles.facilityItem}>
                <div style={styles.facilityIcon}>{i + 1}</div>
                <div style={styles.facilityInfo}>
                  <p style={styles.facilityName}>{f.name}</p>
                  <p style={styles.facilityMeta}>
                    {f.type} • {f.distance_km} km
                  </p>
                  {f.phone && <p style={styles.facilityPhone}>📞 {f.phone}</p>}
                </div>
                <a href={f.google_maps} target="_blank" rel="noreferrer" style={styles.mapsBtn}>
                  Maps →
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <p style={styles.disclaimer}>
        VaaniCare does not replace professional medical advice. Always consult a qualified doctor.
      </p>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "0 0 40px 0",
    maxWidth: 480,
    margin: "0 auto",
    position: "relative",
  },
  blob1: {
    position: "fixed", top: -100, right: -100,
    width: 300, height: 300, borderRadius: "50%",
    background: "radial-gradient(circle, #bbf7d0 0%, transparent 70%)",
    zIndex: 0, pointerEvents: "none",
  },
  blob2: {
    position: "fixed", bottom: -80, left: -80,
    width: 280, height: 280, borderRadius: "50%",
    background: "radial-gradient(circle, #ccfbf1 0%, transparent 70%)",
    zIndex: 0, pointerEvents: "none",
  },
  topBar: {
    width: "100%", display: "flex", alignItems: "center",
    justifyContent: "space-between", padding: "16px 20px",
    zIndex: 1,
  },
  backBtn: {
    display: "flex", alignItems: "center", gap: 4,
    background: "none", border: "none", cursor: "pointer",
    color: "#6b7280", fontSize: 13, fontFamily: "Sora, sans-serif",
  },
  logoSmall: { display: "flex", alignItems: "center", gap: 6 },
  logoSmallText: { fontWeight: 700, color: "#14532d", fontSize: 16 },
  newBtn: {
    display: "flex", alignItems: "center", gap: 4,
    background: "#f0fdf4", border: "1px solid #bbf7d0",
    borderRadius: 20, padding: "6px 12px", cursor: "pointer",
    color: "#16a34a", fontSize: 12, fontFamily: "Sora, sans-serif",
  },
  emergencyBanner: {
    width: "calc(100% - 32px)", margin: "0 16px 16px",
    background: "linear-gradient(135deg, #dc2626, #991b1b)",
    borderRadius: 20, padding: "16px 20px",
    display: "flex", alignItems: "center", justifyContent: "space-between",
    zIndex: 1, boxShadow: "0 4px 20px rgba(220,38,38,0.4)",
  },
  emergencyTitle: { color: "white", fontWeight: 700, fontSize: 16 },
  emergencySubtitle: { color: "rgba(255,255,255,0.8)", fontSize: 12, marginTop: 2 },
  callBtn: {
    display: "flex", alignItems: "center", gap: 6,
    background: "white", color: "#dc2626",
    padding: "10px 16px", borderRadius: 12,
    fontWeight: 700, fontSize: 14, textDecoration: "none",
  },
  severityCard: {
    width: "calc(100% - 32px)", margin: "0 16px 16px",
    borderRadius: 24, padding: "24px",
    zIndex: 1, boxShadow: "0 8px 32px rgba(0,0,0,0.15)",
  },
  severityTop: {
    display: "flex", alignItems: "center",
    justifyContent: "space-between", marginBottom: 16,
  },
  severityBadge: {
    padding: "6px 14px", borderRadius: 20,
    fontSize: 13, fontWeight: 700,
  },
  confidenceText: { color: "rgba(255,255,255,0.7)", fontSize: 12 },
  transcriptLabel: { color: "rgba(255,255,255,0.7)", fontSize: 12, marginBottom: 4 },
  transcriptText: {
    color: "white", fontSize: 16, fontWeight: 500,
    fontStyle: "italic", lineHeight: 1.5,
  },
  langBadge: {
    marginTop: 12, display: "inline-block",
    background: "rgba(255,255,255,0.15)",
    color: "white", padding: "4px 10px",
    borderRadius: 10, fontSize: 11,
  },
  card: {
    width: "calc(100% - 32px)", margin: "0 16px 16px",
    background: "white", borderRadius: 20,
    padding: "20px", zIndex: 1,
    boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
    border: "1px solid #f3f4f6",
  },
  cardHeader: {
    display: "flex", alignItems: "center",
    gap: 8, marginBottom: 14,
  },
  cardTitle: { fontSize: 15, fontWeight: 600, color: "#1f2937", flex: 1 },
  listenBtn: {
    display: "flex", alignItems: "center", gap: 4,
    background: "#f0fdf4", border: "1px solid #bbf7d0",
    color: "#16a34a", padding: "6px 12px",
    borderRadius: 20, cursor: "pointer",
    fontSize: 12, fontFamily: "Sora, sans-serif",
  },
  symptomRow: { display: "flex", flexWrap: "wrap", gap: 8 },
  symptomTag: {
    background: "#eff6ff", color: "#1d4ed8",
    padding: "6px 14px", borderRadius: 20,
    fontSize: 13, fontWeight: 500, textTransform: "capitalize",
  },
  durationText: { color: "#6b7280", fontSize: 13, marginTop: 10 },
  responseText: {
    color: "#374151", fontSize: 15,
    lineHeight: 1.7, fontWeight: 400,
  },
  facilityList: { display: "flex", flexDirection: "column", gap: 12 },
  facilityItem: {
    display: "flex", alignItems: "center", gap: 12,
    padding: "12px", borderRadius: 14,
    background: "#f9fafb", border: "1px solid #f3f4f6",
  },
  facilityIcon: {
    width: 32, height: 32, borderRadius: 10,
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    color: "white", display: "flex",
    alignItems: "center", justifyContent: "center",
    fontWeight: 700, fontSize: 14, flexShrink: 0,
  },
  facilityInfo: { flex: 1, minWidth: 0 },
  facilityName: {
    fontWeight: 600, fontSize: 14,
    color: "#1f2937", whiteSpace: "nowrap",
    overflow: "hidden", textOverflow: "ellipsis",
  },
  facilityMeta: { fontSize: 12, color: "#6b7280", marginTop: 2 },
  facilityPhone: { fontSize: 12, color: "#16a34a", marginTop: 2 },
  mapsBtn: {
    background: "#eff6ff", color: "#1d4ed8",
    padding: "6px 10px", borderRadius: 10,
    fontSize: 12, fontWeight: 500,
    textDecoration: "none", whiteSpace: "nowrap",
  },
  disclaimer: {
    fontSize: 11, color: "#9ca3af",
    textAlign: "center", padding: "0 32px",
    marginTop: 8, zIndex: 1,
  },
};
