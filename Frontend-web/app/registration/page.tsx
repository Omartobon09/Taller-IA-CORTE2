'use client'

import React, { useState } from 'react';
import Link from 'next/link';
import styles from '../login/login.module.css';

export default function RegistrationPage() {
  const [cedula, setCedula] = useState('');
  const [telefono, setTelefono] = useState('');
  const [correo, setCorreo] = useState('');
  const [usuario, setUsuario] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();

    const newUser = {
      cedula,
      telefono,
      correo,
      usuario,
      password
    };

    console.log('Usuario registrado localmente:', newUser);

    // API
    /*
    fetch('/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newUser)
    })
      .then(res => res.json())
      .then(data => console.log('Respuesta del backend:', data))
      .catch(error => console.error('Error al registrar:', error));
    */
  };

  return (
    <div className={styles["login-page"]}>
      <div className={styles["login-overlay"]}></div>
      <div className={styles["login-container"]}>
        <h2>Registro</h2>
        <p>Completa los campos para crear una cuenta</p>
        <form onSubmit={handleRegister}>
          <div>
            <label className={styles['login-subtitles']}>Cédula:</label><br />
            <input
              className={styles['login-subtitles']}
              type="text"
              value={cedula}
              onChange={(e) => setCedula(e.target.value)}
              required
            />
          </div>
          <div>
            <label className={styles['login-subtitles']}>Teléfono:</label><br />
            <input
              className={styles['login-subtitles']}
              type="tel"
              value={telefono}
              onChange={(e) => setTelefono(e.target.value)}
              required
            />
          </div>
          <div>
            <label className={styles['login-subtitles']}>Correo:</label><br />
            <input
              className={styles['login-subtitles']}
              type="email"
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              required
            />
          </div>
          <div>
            <label className={styles['login-subtitles']}>Usuario:</label><br />
            <input
              className={styles['login-subtitles']}
              type="text"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              required
            />
          </div>
          <div>
            <label className={styles['login-subtitles']}>Contraseña:</label><br />
            <input
              className={styles['login-subtitles']}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Registrarse</button>
        </form>
        <p style={{ marginTop: '1rem' }}>
          ¿Ya tienes cuenta? <Link href="/login"><b>Inicia sesión</b></Link>
        </p>
      </div>
    </div>
  );
}
