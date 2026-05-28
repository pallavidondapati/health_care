import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Result from './pages/Result';
import HospitalMap from './pages/HospitalMap';
import PhotoAnalysis from './pages/PhotoAnalysis';

export default function App() {
  return (
    <Router>
      <div style={{ minHeight: "100vh", background: "#f0fdf4" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/result" element={<Result />} />
          <Route path="/map" element={<HospitalMap />} />
          <Route path="/photo" element={<PhotoAnalysis />} />
        </Routes>
      </div>
    </Router>
  );
}