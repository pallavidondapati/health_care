import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mic, MicOff, Upload, Heart, Activity, RotateCcw } from 'lucide-react';
import axios from 'axios';

const API = "http://127.0.0.1:8000/api";

const LANGUAGES = [
  { code: "te", label: "తెలుగు" },
  { code: "hi", label: "हिंदी" },
  { code: "en", label: "English" },
  { code: "ta", label: "தமிழ்" },
  { code: "kn", label: "ಕನ್ನಡ" },
];

// Keyframes for spinner and pulse animations
const globalStyles = `
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  @keyframes pulse {
    0% { transform: scale(1); opacity: 0.5; }
    100% { transform: scale(1.5); opacity: 0; }
  }
`;

export default function Home() {
  const [recording, setRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioURL, setAudioURL] = useState(null);
  const [selectedLang, setSelectedLang] = useState("te");

  const [history, setHistory] = useState([]);
  const [accumulatedSymptoms, setAccumulatedSymptoms] = useState([]);
  const [chatLog, setChatLog] = useState([]);
  const [lastResult, setLastResult] = useState(null);
  const [isFollowUp, setIsFollowUp] = useState(false);

  const mediaRecorder = useRef(null);
  const chunks = useRef([]);
  const audioRef = useRef(null);
  const navigate = useNavigate();

  const startRecording = async () => {
    setError(null);
    setAudioBlob(null);
    setAudioURL(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      chunks.current = [];
      mediaRecorder.current.ondataavailable = e => chunks.current.push(e.data);
      mediaRecorder.current.onstop = () => {
        const blob = new Blob(chunks.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        setAudioURL(URL.createObjectURL(blob));
      };
      mediaRecorder.current.start();
      setRecording(true);
    } catch {
      setError("Microphone access denied.");
    }
  };

  const stopRecording = () => {
    mediaRecorder.current?.stop();
    mediaRecorder.current?.stream.getTracks().forEach(t => t.stop());
    setRecording(false);
  };

  const submitAudio = async (blob) => {
    setUploading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("audio", blob, "recording.webm");
      formData.append("history", JSON.stringify(history));
      formData.append("symptoms", JSON.stringify(accumulatedSymptoms));

      const res = await axios.post(
        `${API}/vaanicare?latitude=18.1066&longitude=83.3956&language=${selectedLang}`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      const data = res.data;

      setHistory(data.history || []);
      setAccumulatedSymptoms(data.accumulated_symptoms || []);
      setLastResult(data);
      setIsFollowUp(true);

      setChatLog(prev => [...prev, {
        user: data.transcript,
        assistant: data.response,
        severity: data.severity,
      }]);

      playTTS(data.response, data.language);

    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong.");
    } finally {
      setUploading(false);
      setAudioBlob(null);
      setAudioURL(null);
    }
  };

  const playTTS = async (text, lang) => {
    try {
      const res = await axios.post(
        `${API}/text-to-speech`,
        { text, language: lang },
        { responseType: "blob" }
      );
      const blob = new Blob([res.data], { type: "audio/mpeg" });
      const url = URL.createObjectURL(blob);
      if (audioRef.current) {
        audioRef.current.src = url;
        audioRef.current.load();
        audioRef.current.play();
      }
    } catch (e) {
      console.error("TTS error", e);
    }
  };

  const uploadFile = async (e) => {
    const file = e.target.files[0];
    if (file) await submitAudio(file);
  };

  const resetConversation = () => {
    setHistory([]);
    setAccumulatedSymptoms([]);
    setChatLog([]);
    setLastResult(null);
    setIsFollowUp(false);
    setAudioBlob(null);
    setAudioURL(null);
    setError(null);
  };

  const SEVERITY_COLORS = {
    low: "#16a34a",
    moderate: "#d97706",
    high: "#ea580c",
    emergency: "#dc2626"
  };

  return (
    <div style={styles.container}>
      {/* Inject keyframes */}
      <style>{globalStyles}</style>

      <div style={styles.blob1} />
      <div style={styles.blob2} />

      {/* Header */}
      <div style={styles.header}>
        <div style={styles.logoRow}>
          <div style={styles.logoIcon}>
            <Heart size={22} color="white" fill="white" />
          </div>
          <h1 style={styles.logoText}>VaaniCare</h1>
          {isFollowUp && (
            <button onClick={resetConversation} style={styles.resetBtn}>
              <RotateCcw size={14} /> New
            </button>
          )}
        </div>
        <p style={styles.tagline}>మీ ఆరోగ్య సహాయకుడు • Your Health Assistant</p>
      </div>

      {/* Language Selector — only show on first turn */}
      {!isFollowUp && (
        <div style={styles.langRow}>
          {LANGUAGES.map(l => (
            <button
              key={l.code}
              onClick={() => setSelectedLang(l.code)}
              style={{
                ...styles.langBtn,
                ...(selectedLang === l.code ? styles.langBtnActive : {})
              }}
            >
              {l.label}
            </button>
          ))}
        </div>
      )}

      {/* Chat Log */}
      {chatLog.length > 0 && (
        <div style={styles.chatLog}>
          {chatLog.map((entry, i) => (
            <div key={i} style={styles.chatEntry}>
              <div style={styles.userBubble}>
                <p style={styles.bubbleLabel}>You said:</p>
                <p style={styles.userText}>"{entry.user}"</p>
              </div>
              <div style={{
                ...styles.assistantBubble,
                borderLeft: `3px solid ${SEVERITY_COLORS[entry.severity] || "#16a34a"}`
              }}>
                <div style={styles.severityRow}>
                  <span style={{
                    ...styles.severityPill,
                    background: SEVERITY_COLORS[entry.severity] + "20",
                    color: SEVERITY_COLORS[entry.severity]
                  }}>
                    {entry.severity}
                  </span>
                </div>
                <p style={styles.assistantText}>{entry.assistant}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Mic Card */}
      <div style={styles.card}>
        <p style={styles.instruction}>
          {isFollowUp ? "🎙️ Speak your reply..." : "Describe your symptoms"}
        </p>

        {accumulatedSymptoms.length > 0 && (
          <div style={styles.symptomsRow}>
            {accumulatedSymptoms.map((s, i) => (
              <span key={i} style={styles.symptomChip}>{s}</span>
            ))}
          </div>
        )}

        <div style={styles.micWrapper}>
          {recording && <div style={styles.pulseRing} />}
          <button
            onClick={recording ? stopRecording : startRecording}
            disabled={uploading}
            style={{
              ...styles.micBtn,
              background: recording
                ? "linear-gradient(135deg, #ef4444, #dc2626)"
                : "linear-gradient(135deg, #16a34a, #0d9488)",
            }}
          >
            {uploading ? (
              <div style={styles.spinner} />
            ) : recording ? (
              <MicOff size={44} color="white" />
            ) : (
              <Mic size={44} color="white" />
            )}
          </button>
        </div>

        <p style={styles.micLabel}>
          {recording ? "🔴 Recording... Tap to stop"
           : uploading ? "Analyzing..."
           : isFollowUp ? "Tap to reply"
           : "Tap to speak"}
        </p>

        {audioURL && !uploading && (
          <div style={styles.previewBox}>
            <audio controls src={audioURL} style={{ width: "100%", borderRadius: 12 }} />
            <button onClick={() => submitAudio(audioBlob)} style={styles.analyzeBtn}>
              <Activity size={18} />
              {isFollowUp ? "Send Reply" : "Analyze Symptoms"}
            </button>
          </div>
        )}

        {!uploading && !audioURL && (
          <label style={styles.uploadLabel}>
            <Upload size={18} color="#9ca3af" />
            <span style={{ color: "#9ca3af", fontSize: 14 }}>Upload audio file</span>
            <input type="file" accept="audio/*" style={{ display: "none" }} onChange={uploadFile} />
          </label>
        )}

        {error && (
          <div style={styles.errorBox}>
            <p style={{ color: "#dc2626", fontSize: 13 }}>⚠️ {error}</p>
          </div>
        )}
      </div>

      {/* Quick Actions — below the main card */}
      <div style={styles.quickActions}>
        <button onClick={() => navigate("/map")} style={styles.actionBtn}>
          <span style={styles.actionIcon}>🏥</span>
          <span style={styles.actionLabel}>Find Hospital</span>
        </button>
        <button onClick={() => navigate("/photo")} style={styles.actionBtn}>
          <span style={styles.actionIcon}>📸</span>
          <span style={styles.actionLabel}>Photo Check</span>
        </button>
      </div>

      {/* View Full Result button */}
      {lastResult && (
        <button
          onClick={() => navigate("/result", { state: { data: lastResult } })}
          style={styles.viewResultBtn}
        >
          View Full Report →
        </button>
      )}

      <audio ref={audioRef} style={{ display: "none" }} />

      <p style={styles.disclaimer}>
        VaaniCare does not replace professional medical advice
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
    padding: "32px 16px",
    position: "relative",
    overflow: "hidden",
    maxWidth: 480,
    margin: "0 auto",
  },
  blob1: {
    position: "fixed", top: -120, right: -120,
    width: 400, height: 400, borderRadius: "50%",
    background: "radial-gradient(circle, #bbf7d0 0%, transparent 70%)",
    zIndex: 0, pointerEvents: "none",
  },
  blob2: {
    position: "fixed", bottom: -100, left: -100,
    width: 350, height: 350, borderRadius: "50%",
    background: "radial-gradient(circle, #ccfbf1 0%, transparent 70%)",
    zIndex: 0, pointerEvents: "none",
  },
  header: {
    textAlign: "center", marginBottom: 20, zIndex: 1, width: "100%",
  },
  logoRow: {
    display: "flex", alignItems: "center",
    justifyContent: "center", gap: 10, marginBottom: 6,
  },
  logoIcon: {
    width: 40, height: 40, borderRadius: 12,
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    display: "flex", alignItems: "center", justifyContent: "center",
    boxShadow: "0 4px 12px rgba(22,163,74,0.4)",
  },
  logoText: {
    fontSize: 32, fontWeight: 700, color: "#14532d", letterSpacing: "-1px",
  },
  resetBtn: {
    display: "flex", alignItems: "center", gap: 4,
    background: "#f0fdf4", border: "1px solid #bbf7d0",
    borderRadius: 20, padding: "6px 12px",
    cursor: "pointer", color: "#16a34a",
    fontSize: 12, fontFamily: "Sora, sans-serif",
  },
  tagline: { fontSize: 13, color: "#6b7280" },
  langRow: {
    display: "flex", gap: 8, marginBottom: 20,
    flexWrap: "wrap", justifyContent: "center", zIndex: 1,
  },
  langBtn: {
    padding: "6px 14px", borderRadius: 20,
    border: "1.5px solid #d1fae5", background: "white",
    color: "#6b7280", fontSize: 13, fontWeight: 500, cursor: "pointer",
  },
  langBtnActive: {
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    border: "1.5px solid transparent", color: "white",
    boxShadow: "0 2px 8px rgba(22,163,74,0.3)",
  },
  chatLog: {
    width: "100%", display: "flex", flexDirection: "column",
    gap: 16, marginBottom: 16, zIndex: 1,
  },
  chatEntry: { display: "flex", flexDirection: "column", gap: 8 },
  userBubble: {
    background: "#f3f4f6", borderRadius: "16px 16px 4px 16px",
    padding: "12px 16px", alignSelf: "flex-end", maxWidth: "85%",
  },
  bubbleLabel: { fontSize: 11, color: "#9ca3af", marginBottom: 4 },
  userText: { fontSize: 14, color: "#374151", fontStyle: "italic" },
  assistantBubble: {
    background: "white", borderRadius: "4px 16px 16px 16px",
    padding: "12px 16px", alignSelf: "flex-start", maxWidth: "90%",
    boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
  },
  severityRow: { marginBottom: 6 },
  severityPill: {
    fontSize: 11, fontWeight: 600, padding: "2px 10px",
    borderRadius: 10, textTransform: "capitalize",
  },
  assistantText: { fontSize: 14, color: "#374151", lineHeight: 1.6 },
  card: {
    background: "white", borderRadius: 28,
    boxShadow: "0 8px 40px rgba(0,0,0,0.08)",
    padding: "28px 24px", width: "100%",
    display: "flex", flexDirection: "column",
    alignItems: "center", zIndex: 1,
    border: "1px solid #f0fdf4",
  },
  instruction: {
    fontSize: 15, color: "#374151",
    marginBottom: 16, fontWeight: 500,
  },
  symptomsRow: {
    display: "flex", flexWrap: "wrap", gap: 6,
    marginBottom: 16, justifyContent: "center",
  },
  symptomChip: {
    background: "#eff6ff", color: "#1d4ed8",
    padding: "4px 12px", borderRadius: 20,
    fontSize: 12, fontWeight: 500, textTransform: "capitalize",
  },
  micWrapper: {
    position: "relative", display: "flex",
    alignItems: "center", justifyContent: "center", marginBottom: 12,
  },
  pulseRing: {
    position: "absolute", inset: -12, borderRadius: "50%",
    border: "3px solid #ef4444", opacity: 0.5,
    animation: "pulse 1.5s ease-out infinite",
  },
  micBtn: {
    width: 110, height: 110, borderRadius: "50%",
    border: "none", cursor: "pointer",
    display: "flex", alignItems: "center", justifyContent: "center",
    boxShadow: "0 8px 32px rgba(22,163,74,0.35)",
    transition: "all 0.3s ease", position: "relative", zIndex: 1,
  },
  spinner: {
    width: 32, height: 32,
    border: "3px solid rgba(255,255,255,0.3)",
    borderTop: "3px solid white", borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  micLabel: { fontSize: 13, color: "#6b7280", marginBottom: 16 },
  previewBox: {
    width: "100%", display: "flex",
    flexDirection: "column", gap: 10, marginBottom: 12,
  },
  analyzeBtn: {
    width: "100%", padding: "13px",
    borderRadius: 14, border: "none",
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    color: "white", fontSize: 15, fontWeight: 600,
    cursor: "pointer", display: "flex",
    alignItems: "center", justifyContent: "center", gap: 8,
  },
  uploadLabel: {
    display: "flex", alignItems: "center", gap: 8,
    border: "2px dashed #e5e7eb", borderRadius: 14,
    padding: "14px 20px", cursor: "pointer",
    width: "100%", justifyContent: "center",
  },
  errorBox: {
    marginTop: 12, background: "#fef2f2",
    border: "1px solid #fecaca", borderRadius: 12,
    padding: "10px 14px", width: "100%",
  },
  // Quick Actions
  quickActions: {
    display: "flex", gap: 12, marginTop: 16, zIndex: 1, width: "100%",
  },
  actionBtn: {
    flex: 1, display: "flex", flexDirection: "column",
    alignItems: "center", gap: 6, padding: "16px 12px",
    background: "white", borderRadius: 20,
    border: "1px solid #f0fdf4", cursor: "pointer",
    boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
  },
  actionIcon: { fontSize: 24 },
  actionLabel: { fontSize: 12, fontWeight: 600, color: "#374151" },
  viewResultBtn: {
    marginTop: 16, padding: "12px 24px",
    borderRadius: 20, border: "1px solid #bbf7d0",
    background: "white", color: "#16a34a",
    fontSize: 14, fontWeight: 600, cursor: "pointer",
    zIndex: 1,
  },
  disclaimer: {
    marginTop: 20, fontSize: 11,
    color: "#9ca3af", textAlign: "center", zIndex: 1,
  },
};