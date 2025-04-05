"use client";

import React, { useState, useEffect } from "react";
import styles from "../../style.module.css";
import { doctors } from "../quotes/doctors";

interface MedicalHistory {
  id: number;
  doctorId: number;
  diagnosis: string;
  recommendations: string;
  imageUrl?: string;
  date: string;
  time: string; 
}

export default function HistoryPage() {
  const [history, setHistory] = useState<MedicalHistory[]>([]);

  useEffect(() => {
    // Datos locales
    const mockHistory: MedicalHistory[] = [
      {
        id: 1,
        doctorId: 101,
        diagnosis: "Gripe común",
        recommendations: "Reposo, líquidos y paracetamol.",
        imageUrl: "",
        date: "2025-03-30",
        time: "09:00"
      },
      {
        id: 2,
        doctorId: 102,
        diagnosis: "Dolor lumbar",
        recommendations: "Fisioterapia y analgésicos.",
        imageUrl: "",
        date: "2025-04-02",
        time: "14:30"
      }
    ];
    setHistory(mockHistory);

    // API
    /*
    const fetchHistory = async () => {
      try {
        const res = await fetch("/api/history");
        if (!res.ok) throw new Error("Error al obtener historial");
        const data = await res.json();
        setHistory(data);
      } catch (err) {
        console.error("Error:", err);
      }
    };

    fetchHistory();
    */
  }, []);

  return (
    <div className={styles["home-container"]}>
      <div className={styles["container-box"]}>
        <h2>Historial Médico</h2>
        <p>Consulta tus diagnósticos anteriores, recomendaciones y archivos relacionados.</p>

        {history.length === 0 ? (
          <p>No tienes historial médico disponible.</p>
        ) : (
          <ul className={styles["appointment-form"]}>
            {history.map((item) => {
              const doctor = doctors.find((doc) => doc.id === item.doctorId);
              return (
                <li key={item.id} style={{ marginBottom: "1.5rem", borderBottom: "1px solid #ccc", paddingBottom: "1rem" }}>
                  <strong>Médico:</strong> {doctor?.name} - {doctor?.specialty}<br />
                  <strong>Fecha:</strong> {item.date} a las {item.time}<br />
                  <strong>Diagnóstico:</strong> {item.diagnosis}<br />
                  <strong>Recomendaciones:</strong> {item.recommendations}<br />
                  {item.imageUrl && (
                    <div style={{ marginTop: "0.5rem" }}>
                      <strong>Imagen:</strong><br />
                      <img src={item.imageUrl} alt="Diagnóstico" width="150" />
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
}
