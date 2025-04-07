"use client";

import React, { useState } from "react";
import Link from "next/link";
import styles from "../style.module.css";

export default function RegistrationPage() {
  const [cedula, setCedula] = useState("");
  const [telefono, setTelefono] = useState("");
  const [correo, setCorreo] = useState("");
  const [nombre, setNombre] = useState("");
  const [password, setPassword] = useState("");
  const [fechaNacimiento, setFechaNacimiento] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    const nuevoUsuario = {
      nombre,
      email: correo,
      password,
      documento: cedula,
      telefono,
      fecha_nacimiento: new Date(fechaNacimiento).toISOString(),
      rol_id: 2,
      especialidad: "",
      creado_en: new Date().toISOString(),
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/post/usuarios", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(nuevoUsuario),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Error en el registro");
      }

      alert("Registro exitoso. Ahora puedes iniciar sesión.");
    } catch (error: any) {
      alert("Error al registrar: " + error.message);
    }
  };

  return (
    <div className={styles["container-registration"]}>
      <div className={styles["login-page"]}>
        <div className={styles["login-container"]}>
          <h2>Registro</h2>
          <p>Completa los campos para crear una cuenta</p>
          <form onSubmit={handleRegister}>
            <div className={styles["container-label"]}>
              <label className={styles["login-subtitles"]}>Nombre:</label>
              <br />
              <input
                className={styles["login-subtitles"]}
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
              />
            </div>
            <div className={styles["container-label"]}>
              <label className={styles["login-subtitles"]}>Correo:</label>
              <br />
              <input
                className={styles["login-subtitles"]}
                type="email"
                value={correo}
                onChange={(e) => setCorreo(e.target.value)}
                required
              />
            </div>
            <div className={styles["container-label"]}>
              <label className={styles["login-subtitles"]}>Contraseña:</label>
              <br />
              <input
                className={styles["login-subtitles"]}
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className={styles["container-label"]}>
              <label className={styles["login-subtitles"]}>Cédula:</label>
              <br />
              <input
                className={styles["login-subtitles"]}
                type="text"
                value={cedula}
                onChange={(e) => setCedula(e.target.value)}
                required
              />
            </div>
            <div className={styles["container-label"]}>
              <label className={styles["login-subtitles"]}>Teléfono:</label>
              <br />
              <input
                className={styles["login-subtitles"]}
                type="tel"
                value={telefono}
                onChange={(e) => setTelefono(e.target.value)}
                required
              />
            </div>
            <div className={styles["container-label"]}>
              <label className={styles["login-subtitles"]}>
                Fecha de nacimiento:
              </label>
              <br />
              <input
                className={styles["login-subtitles"]}
                type="date"
                value={fechaNacimiento}
                onChange={(e) => setFechaNacimiento(e.target.value)}
                required
              />
            </div>
            <button type="submit">Registrarse</button>
          </form>
          <p style={{ marginTop: "1rem" }}>
            ¿Ya tienes cuenta?{" "}
            <Link href="/login">
              <b>Inicia sesión</b>
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
