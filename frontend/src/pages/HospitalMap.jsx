import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, MapPin, Navigation } from "lucide-react";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix leaflet marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Custom hospital marker
const hospitalIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const userIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const API = "http://127.0.0.1:8000/api";

// FIX 4: Add keyframes for spinner animation via a style tag
const spinnerStyle = `
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`;

export default function HospitalMap() {
  const [location, setLocation] = useState(null);
  const [facilities, setFacilities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [severity, setSeverity] = useState("moderate");
  const navigate = useNavigate();

  useEffect(() => {
    getUserLocation();
  }, []);

  const getUserLocation = () => {
    setLoading(true);
    if (!navigator.geolocation) {
      fetchFacilities(18.1066, 83.3956, severity);
      return;
    }
    navigator.geolocation.getCurrentPosition(
      pos => fetchFacilities(pos.coords.latitude, pos.coords.longitude, severity),
      () => fetchFacilities(18.1066, 83.3956, severity) // fallback
    );
  };

  // FIX 3: Accept `sev` param so severity filter change is not stale
  const fetchFacilities = async (lat, lon, sev = severity) => {
    setLocation({ lat, lon });
    try {
      const res = await fetch(
        `${API}/nearest-facility`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ latitude: lat, longitude: lon, severity: sev })
        }
      );
      const data = await res.json();
      setFacilities(data.facilities || []);
    } catch (e) {
      setError("Could not load facilities");
    } finally {
      setLoading(false);
    }
  };

  const SEVERITY_OPTIONS = [
    { value: "low", label: "Pharmacy", color: "#16a34a" },
    { value: "moderate", label: "Clinic/PHC", color: "#d97706" },
    { value: "high", label: "Hospital", color: "#ea580c" },
    { value: "emergency", label: "Emergency", color: "#dc2626" },
  ];

  return (
    <div style={styles.container}>
      {/* FIX 4: Inject keyframes for spinner */}
      <style>{spinnerStyle}</style>

      {/* Header */}
      <div style={styles.topBar}>
        <button onClick={() => navigate("/")} style={styles.backBtn}>
          <ArrowLeft size={16} /> Back
        </button>
        <h2 style={styles.title}>Nearby Facilities</h2>
        <button onClick={getUserLocation} style={styles.refreshBtn}>
          <Navigation size={14} />
        </button>
      </div>

      {/* Severity Filter */}
      <div style={styles.filterRow}>
        {SEVERITY_OPTIONS.map(s => (
          <button
            key={s.value}
            onClick={() => {
              setSeverity(s.value);
              // FIX 3: Pass s.value directly instead of relying on stale state
              if (location) fetchFacilities(location.lat, location.lon, s.value);
            }}
            style={{
              ...styles.filterBtn,
              background: severity === s.value ? s.color : "white",
              color: severity === s.value ? "white" : "#6b7280",
              border: `1.5px solid ${severity === s.value ? s.color : "#e5e7eb"}`,
            }}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* Map */}
      {loading ? (
        <div style={styles.loadingBox}>
          <div style={styles.spinner} />
          <p style={styles.loadingText}>Finding your location...</p>
        </div>
      ) : error ? (
        <div style={styles.errorBox}>
          <p style={{ color: "#dc2626" }}>{error}</p>
        </div>
      ) : location ? (
        <div style={styles.mapWrapper}>
          <MapContainer
            center={[location.lat, location.lon]}
            zoom={13}
            style={{ height: "100%", width: "100%", borderRadius: 20 }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; OpenStreetMap contributors'
            />

            {/* User location */}
            <Marker position={[location.lat, location.lon]} icon={userIcon}>
              <Popup>
                <div style={{ textAlign: "center" }}>
                  <p style={{ fontWeight: 700, color: "#16a34a" }}>📍 You are here</p>
                </div>
              </Popup>
            </Marker>

            {/* 10km radius circle */}
            <Circle
              center={[location.lat, location.lon]}
              radius={10000}
              pathOptions={{ color: "#16a34a", fillColor: "#16a34a", fillOpacity: 0.05 }}
            />

            {/* Hospital markers */}
            {facilities.map((f, i) => (
              <Marker
                key={i}
                position={[f.latitude, f.longitude]}
                icon={hospitalIcon}
              >
                <Popup>
                  <div style={{ minWidth: 180 }}>
                    <p style={{ fontWeight: 700, fontSize: 14, marginBottom: 4 }}>{f.name}</p>
                    <p style={{ fontSize: 12, color: "#6b7280", textTransform: "capitalize", marginBottom: 4 }}>
                      {f.type} • {f.distance_km} km away
                    </p>
                    {f.phone && (
                      <a href={`tel:${f.phone}`} style={{ fontSize: 12, color: "#16a34a", display: "block", marginBottom: 4 }}>
                        📞 {f.phone}
                      </a>
                    )}
                    {/* FIX 1: Added missing opening <a> tag */}
                    <a
                      href={f.google_maps}
                      target="_blank"
                      rel="noreferrer"
                      style={{
                        display: "block", textAlign: "center",
                        background: "#16a34a", color: "white",
                        padding: "6px", borderRadius: 8,
                        fontSize: 12, textDecoration: "none",
                        marginTop: 6,
                      }}
                    >
                      Get Directions →
                    </a>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      ) : null}

      {/* Facility List */}
      <div style={styles.listContainer}>
        <h3 style={styles.listTitle}>
          <MapPin size={16} color="#dc2626" />
          {facilities.length} facilities found nearby
        </h3>

        {facilities.length === 0 ? (
          <p style={styles.emptyText}>No facilities found in 10km radius</p>
        ) : (
          facilities.map((f, i) => (
            <div key={i} style={styles.facilityCard}>
              <div style={styles.facilityNum}>{i + 1}</div>
              <div style={styles.facilityInfo}>
                <p style={styles.facilityName}>{f.name}</p>
                <p style={styles.facilityMeta}>
                  {f.type} • {f.distance_km} km
                </p>
                {f.phone && (
                  <a href={`tel:${f.phone}`} style={styles.facilityPhone}>
                    📞 {f.phone}
                  </a>
                )}
              </div>
              {/* FIX 2: Added missing opening <a> tag */}
              <a
                href={f.google_maps}
                target="_blank"
                rel="noreferrer"
                style={styles.directionsBtn}
              >
                Go →
              </a>
            </div>
          ))
        )}

        {/* Emergency */}
        <a href="tel:108" style={styles.emergencyBtn}>
          🚨 Call 108 — Emergency Ambulance
        </a>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh", display: "flex", flexDirection: "column",
    alignItems: "center", maxWidth: 480, margin: "0 auto",
    background: "#f0fdf4",
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
  refreshBtn: {
    width: 36, height: 36, borderRadius: 10,
    background: "#f0fdf4", border: "1px solid #bbf7d0",
    display: "flex", alignItems: "center", justifyContent: "center",
    cursor: "pointer", color: "#16a34a",
  },
  filterRow: {
    display: "flex", gap: 8, padding: "12px 16px",
    width: "100%", overflowX: "auto",
  },
  filterBtn: {
    padding: "6px 14px", borderRadius: 20,
    fontSize: 12, fontWeight: 500, cursor: "pointer",
    whiteSpace: "nowrap", fontFamily: "Sora, sans-serif",
    transition: "all 0.2s",
  },
  mapWrapper: {
    width: "calc(100% - 32px)", height: 300,
    margin: "0 16px 16px", borderRadius: 20,
    overflow: "hidden", boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
  },
  loadingBox: {
    display: "flex", flexDirection: "column",
    alignItems: "center", gap: 12, padding: 40,
  },
  spinner: {
    width: 36, height: 36,
    border: "3px solid #e5e7eb",
    borderTop: "3px solid #16a34a",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  loadingText: { color: "#6b7280", fontSize: 14 },
  errorBox: { padding: 20, textAlign: "center" },
  listContainer: {
    width: "calc(100% - 32px)", margin: "0 16px",
    display: "flex", flexDirection: "column", gap: 10,
  },
  listTitle: {
    display: "flex", alignItems: "center", gap: 6,
    fontSize: 15, fontWeight: 600, color: "#1f2937", marginBottom: 4,
  },
  emptyText: { fontSize: 13, color: "#9ca3af", textAlign: "center", padding: 12 },
  facilityCard: {
    display: "flex", alignItems: "center", gap: 12,
    padding: "12px", background: "white", borderRadius: 16,
    boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
  },
  facilityNum: {
    width: 32, height: 32, borderRadius: 10,
    background: "linear-gradient(135deg, #16a34a, #0d9488)",
    color: "white", fontWeight: 700, fontSize: 14,
    display: "flex", alignItems: "center", justifyContent: "center",
    flexShrink: 0,
  },
  facilityInfo: { flex: 1, minWidth: 0 },
  facilityName: {
    fontWeight: 600, fontSize: 14, color: "#1f2937",
    whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
  },
  facilityMeta: { fontSize: 12, color: "#6b7280", marginTop: 2 },
  facilityPhone: { fontSize: 12, color: "#16a34a", marginTop: 2, display: "block" },
  directionsBtn: {
    background: "#eff6ff", color: "#1d4ed8",
    padding: "6px 12px", borderRadius: 10,
    fontSize: 12, fontWeight: 600, textDecoration: "none",
    whiteSpace: "nowrap",
  },
  emergencyBtn: {
    display: "block", textAlign: "center",
    background: "linear-gradient(135deg, #dc2626, #991b1b)",
    color: "white", padding: "16px",
    borderRadius: 16, fontSize: 15, fontWeight: 700,
    textDecoration: "none", marginTop: 8, marginBottom: 24,
    boxShadow: "0 4px 16px rgba(220,38,38,0.3)",
  },
};