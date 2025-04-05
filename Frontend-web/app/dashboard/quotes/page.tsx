"use client";

import React, { useState } from "react";
import styles from "../../style.module.css";
import { doctors } from "./doctors";

// interface para usar en futuro con API
interface Appointment {
  doctorId: number;
  date: string;
  time: string;
}

export default function QuotesPage() {
  const [selectedDoctor, setSelectedDoctor] = useState<number | null>(null);
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTime, setSelectedTime] = useState("");
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [error, setError] = useState("");

  const availableTimes = [
    "08:00", "08:30", "09:00", "09:30", "10:00",
    "10:30", "11:00", "11:30", "12:00", "12:30",
    "13:00", "13:30", "14:00", "14:30", "15:00"
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedDoctor || !selectedDate || !selectedTime) return;

    const conflict = appointments.find(
      (appt) =>
        appt.doctorId === selectedDoctor &&
        appt.date === selectedDate &&
        appt.time === selectedTime
    );

    if (conflict) {
      setError("Esta cita ya fue reservada por otro paciente.");
      return;
    }

    // Datos locales
    setAppointments([
      ...appointments,
      { doctorId: selectedDoctor, date: selectedDate, time: selectedTime }
    ]);

    setError("");

    // API
    /*
    try {
      const res = await fetch("/api/appointments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          doctorId: selectedDoctor,
          date: selectedDate,
          time: selectedTime,
        }),
      });

      if (!res.ok) throw new Error("Error al reservar la cita");

      const newAppointment = await res.json();
      setAppointments(prev => [...prev, newAppointment]);
    } catch (err) {
      setError("Error al conectar con el servidor.");
    }
    */
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
            <option value="" disabled>Selecciona un médico</option>
            {doctors.map((doctor) => (
              <option key={doctor.id} value={doctor.id}>
                {doctor.name} - {doctor.specialty}
              </option>
            ))}
          </select>

          <label>Fecha:</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            required
          />

          <label>Hora:</label>
          <select
            value={selectedTime}
            onChange={(e) => setSelectedTime(e.target.value)}
            required
          >
            <option value="" disabled>Selecciona una hora</option>
            {availableTimes.map((time) => (
              <option key={time} value={time}>{time}</option>
            ))}
          </select>

          {error && <p style={{ color: "red" }}>{error}</p>}

          <button type="submit" className={styles["login-button"]}>
            Reservar Cita
          </button>
        </form>

        <hr style={{ marginTop: "2rem", marginBottom: "1rem" }} />

        <h3>Citas Reservadas:</h3>
        <ul>
          {appointments.map((appt, idx) => {
            const doctor = doctors.find(d => d.id === appt.doctorId);
            return (
              <li key={idx}>
                {doctor?.name} - {appt.date} a las {appt.time}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
