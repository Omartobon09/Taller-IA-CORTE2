"use client";

import React, { useEffect, useState } from "react";
import styles from "../../style.module.css";

// Interfaces
interface Doctor {
  id: number;
  nombre: string;
  email: string;
  documento: string;
  telefono: string;
  especialidad: string;
}

interface ReservedAppointment {
  medico_id: number;
  fecha: string;
  hora: string | number;
  estado: string;
}

export default function QuotesPage() {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [selectedDoctor, setSelectedDoctor] = useState<number | null>(null);
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTime, setSelectedTime] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [reservedAppointments, setReservedAppointments] = useState<
    ReservedAppointment[]
  >([]);

  const availableTimes = [
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
  ];

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const res = await fetch("http://localhost:8000/get/medicos");
        const data = await res.json();
        setDoctors(data.resultado);
      } catch (err) {
        console.error("Error al obtener los médicos:", err);
      }
    };

    fetchDoctors();
  }, []);

  useEffect(() => {
    const fetchReservedAppointments = async () => {
      const pacienteId = localStorage.getItem("user_id");
      if (!pacienteId) return;

      try {
        const res = await fetch(
          `http://localhost:8000/get/citas/paciente/${pacienteId}`
        );
        const data = await res.json();
        const resultado = Array.isArray(data.resultado) ? data.resultado : [];
        setReservedAppointments(resultado);
      } catch (err) {
        console.error("Error al obtener las citas reservadas:", err);
        setReservedAppointments([]); // también protegemos en caso de error
      }
    };

    fetchReservedAppointments();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const pacienteId = localStorage.getItem("user_id");
    if (!pacienteId) {
      setError("Usuario no autenticado.");
      return;
    }

    if (!selectedDoctor || !selectedDate || !selectedTime) {
      setError("Por favor completa todos los campos.");
      return;
    }

    try {
      const disponibilidadRes = await fetch(
        `http://localhost:8000/verificar-disponibilidad?medico_id=${selectedDoctor}&fecha=${selectedDate}&hora=${selectedTime}`
      );

      const disponible = await disponibilidadRes.json();

      if (!disponible) {
        setError("Este horario ya está reservado.");
        return;
      }

      const cita = {
        paciente_id: Number(pacienteId),
        medico_id: selectedDoctor,
        fecha: selectedDate,
        hora: selectedTime,
        estado: "Pendiente",
      };

      const res = await fetch("http://localhost:8000/post/citas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(cita),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Error al reservar la cita");
      }

      setSuccess("Cita reservada exitosamente.");
      setSelectedDoctor(null);
      setSelectedDate("");
      setSelectedTime("");

      const citasRes = await fetch(
        `http://localhost:8000/get/citas/paciente/${pacienteId}`
      );
      const citasData = await citasRes.json();
      setReservedAppointments(citasData.resultado || citasData);
    } catch (err: any) {
      console.error("Error al reservar cita:", err);
      setError(err.message || "Error inesperado.");
    }
  };

  const getDoctorNameById = (id: number) => {
    const doctor = doctors.find((d) => d.id === id);
    return doctor ? doctor.nombre : `ID ${id}`;
  };

  const formatTime = (hora: string | number): string => {
    const segundos = typeof hora === "string" ? parseInt(hora) : hora;
    const horas = Math.floor(segundos / 3600)
      .toString()
      .padStart(2, "0");
    const minutos = Math.floor((segundos % 3600) / 60)
      .toString()
      .padStart(2, "0");
    return `${horas}:${minutos}`;
  };

  return (
    <div className={styles["home-container"]}>
      <div className={styles["container-box"]}>
        <h2>Reservar Cita Médica</h2>
        <p>Selecciona un médico, fecha y hora para tu cita.</p>

        <form onSubmit={handleSubmit} className={styles["appointment-form"]}>
          <label>Médico:</label>
          <select
            value={selectedDoctor ?? ""}
            onChange={(e) => setSelectedDoctor(Number(e.target.value))}
            required
          >
            <option value="" disabled>
              Selecciona un médico
            </option>
            {doctors.map((doctor) => (
              <option key={doctor.id} value={doctor.id}>
                {doctor.nombre} - {doctor.especialidad}
              </option>
            ))}
          </select>

          <label>Fecha:</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            required
            min={new Date().toISOString().split("T")[0]}
          />

          <label>Hora:</label>
          <select
            value={selectedTime}
            onChange={(e) => setSelectedTime(e.target.value)}
            required
          >
            <option value="" disabled>
              Selecciona una hora
            </option>
            {availableTimes.map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>

          {error && <p style={{ color: "red" }}>{error}</p>}
          {success && <p style={{ color: "green" }}>{success}</p>}

          <button type="submit" className={styles["login-button"]}>
            Reservar Cita
          </button>
        </form>

        <hr style={{ marginTop: "2rem", marginBottom: "1rem" }} />

        <h3>Citas Reservadas:</h3>
        <ul>
          {reservedAppointments.length === 0 ? (
            <li>No tienes citas reservadas.</li>
          ) : (
            reservedAppointments.map((appt, idx) => (
              <li key={idx}>
                {getDoctorNameById(appt.medico_id)} - {appt.fecha} a las{" "}
                {formatTime(appt.hora)} ({appt.estado})
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}
