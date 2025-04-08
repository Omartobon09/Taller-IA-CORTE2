"use client";

import React, { useState, useEffect } from "react";
import styles from "../../style.module.css";

interface MedicalHistory {
  id: number;
  paciente_id: number;
  medico_id: number;
  diagnostico: string;
  recomendaciones: string;
  fecha: string;
}

interface Doctor {
  id: number;
  nombre: string;
  email: string;
  documento: string;
  telefono: string;
  especialidad: string;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<MedicalHistory[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [patientName, setPatientName] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Obtener el nombre del paciente desde localStorage
    const nombrePaciente = localStorage.getItem('user_name');
    if (nombrePaciente) {
      setPatientName(nombrePaciente);
    }

    // Función para obtener la lista de médicos
    const fetchMedicos = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/get/medicos');
        
        if (!response.ok) {
          throw new Error(`Error al obtener médicos: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.resultado && Array.isArray(data.resultado)) {
          setDoctors(data.resultado);
        } else if (Array.isArray(data)) {
          setDoctors(data);
        } else {
          console.warn("Formato de datos de médicos inesperado:", data);
          setDoctors([]);
        }
      } catch (err) {
        console.error("Error al obtener médicos:", err);
      }
    };

    // Función para obtener el historial médico
    const fetchHistorialMedico = async () => {
      try {
        const pacienteId = localStorage.getItem('user_id');
        
        if (!pacienteId) {
          throw new Error("No se encontró ID de paciente en localStorage");
        }
        
        const apiUrl = `http://127.0.0.1:8000/get/historiales/paciente/${pacienteId}`;
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
          throw new Error(`Error en la respuesta: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.resultado && Array.isArray(data.resultado)) {
          setHistory(data.resultado);
        } else if (Array.isArray(data)) {
          setHistory(data);
        } else {
          setHistory([]);
          console.warn("Formato de datos de historial inesperado:", data);
        }
      } catch (err) {
        console.error("Error al obtener historial:", err);
        setError(`Error al obtener el historial médico: ${err instanceof Error ? err.message : String(err)}`);
      } finally {
        setLoading(false);
      }
    };
    
    // Ejecutar ambas consultas en paralelo
    Promise.all([fetchMedicos(), fetchHistorialMedico()]).catch(error => {
      console.error("Error en carga inicial:", error);
      setLoading(false);
    });
  }, []);

  // Función para formatear la fecha
  const formatearFecha = (fechaString: string) => {
    try {
      const fecha = new Date(fechaString);
      if (isNaN(fecha.getTime())) {
        return fechaString;
      }
      
      const opciones: Intl.DateTimeFormatOptions = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      return fecha.toLocaleDateString('es-ES', opciones);
    } catch (e) {
      return fechaString;
    }
  };

  // Función para encontrar el nombre del médico por ID
  const getDoctorName = (medicoId: number) => {
    const doctor = doctors.find(doc => doc.id === medicoId);
    return doctor ? doctor.nombre : `Médico ID: ${medicoId}`;
  };

  // Función para encontrar la especialidad del médico por ID
  const getDoctorSpecialty = (medicoId: number) => {
    const doctor = doctors.find(doc => doc.id === medicoId);
    return doctor ? doctor.especialidad : "No especificada";
  };

  if (loading) {
    return (
      <div className={styles["home-container"]}>
        <div className={styles["container-box"]}>
          <h2>Cargando historial médico...</h2>
          <p>Obteniendo información del paciente y médicos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles["home-container"]}>
        <div className={styles["container-box"]}>
          <h2>Error</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles["home-container"]}>
      <div className={styles["container-box"]}>
        <h2>Historial Médico de {patientName}</h2>
        <p>Consulta tus diagnósticos anteriores, recomendaciones y archivos relacionados.</p>
        
        {history.length === 0 ? (
          <p>No tienes historial médico disponible.</p>
        ) : (
          <ul className={styles["appointment-form"]}>
            {history.map((item) => (
              <li key={item.id} style={{ marginBottom: "1.5rem", borderBottom: "1px solid #ccc", paddingBottom: "1rem" }}>
                <strong>Paciente:</strong> {patientName}<br />
                <strong>Médico:</strong> {getDoctorName(item.medico_id)} - {getDoctorSpecialty(item.medico_id)}<br />
                <strong>Fecha:</strong> {formatearFecha(item.fecha)}<br />
                <strong>Diagnóstico:</strong> {item.diagnostico}<br />
                <strong>Recomendaciones:</strong> {item.recomendaciones}<br />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}