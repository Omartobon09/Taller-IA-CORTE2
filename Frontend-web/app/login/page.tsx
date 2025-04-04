'use client'

import { useState } from 'react';
import styles from './login.module.css';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Email:', email);
    console.log('Password:', password);
  };

  return (
    <div className={styles["login-page"]}>
      <div className={styles["login-overlay"]}></div>
      <div className={styles["login-container"]}>
        <h2>Iniciar sesión</h2>
        <p>Ingresa tu <b>usuario</b> y <b>contraseña</b> para poder ingresar al sistema</p>
        <form onSubmit={handleLogin}>
          <div>
            <label className={styles['login-subtitles']}>Email:</label><br />
            <input className={styles['login-subtitles']}
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label className={styles['login-subtitles']}>Contraseña:</label><br />
            <input className={styles['login-subtitles']}
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">
            Iniciar sesión
          </button>
        </form>
      </div>
    </div>
  );
}
