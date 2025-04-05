"use client";

import React from "react";
import styles from "../style.module.css";
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className={styles["home-container"]}>
      <div className={styles["container-box"]}>
        <h2>Bienvenido al Sistema Inteligente de Salud</h2>
        <p>
          Este sistema está diseñado para ayudarte a comprender mejor el
          funcionamiento del cuerpo humano, especialmente el{" "}
          <strong>sistema circulatorio</strong>.
        </p>

        <div style={{ marginTop: "1.5rem", textAlign: "left" }}>
          <h3>Principales enfermedades del sistema circulatorio:</h3>
          <ul>
            <li>
              <strong>Hipertensión arterial:</strong> Presión elevada de forma
              continua.
            </li>
            <li>
              <strong>Infarto al miocardio:</strong> Bloqueo del flujo sanguíneo
              al corazón.
            </li>
            <li>
              <strong>Insuficiencia cardíaca:</strong> El corazón no bombea
              sangre eficientemente.
            </li>
            <li>
              <strong>Arritmias:</strong> Latidos irregulares del corazón.
            </li>
            <li>
              <strong>Arteriosclerosis:</strong> Endurecimiento de arterias por
              placas de grasa.
            </li>
          </ul>
        </div>

        <div style={{ marginTop: "2rem" }}>
          <p>
            <strong>Selecciona una opción del menú:</strong>
          </p>
          
          <br />
          <Link href="/dashboard/quotes">
            <button className={styles["login-button"]}>Reservar Cita</button>
          </Link>
          <br />
          <Link href="/dashboard/history">
            <button className={styles["login-button"]}>Historial</button>
          </Link>
        </div>
      </div>
    </div>
  );
}
