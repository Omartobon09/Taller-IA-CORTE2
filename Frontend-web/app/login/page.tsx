'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import styles from '../style.module.css';

export default function LoginPage() {
  const router = useRouter();

  // Datos locales
  const [users] = useState([
    { user: 'admin', password: '123456' },
    { user: 'nicolas', password: 'abc123' }
  ]);

  const [user, setUser] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validación local
    const foundUser = users.find(
      u => u.user === user && u.password === password
    );

    if (foundUser) {
      alert('Inicio de sesión exitoso');
      router.push('/dashboard');
    } else {
      alert('Usuario o contraseña incorrectos');
    }

    // API

    /*
    try {
      const res = await fetch('http://localhost:3000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user, password }),
      });

      if (!res.ok) throw new Error('Credenciales incorrectas');

      const data = await res.json();
      console.log('Token recibido:', data.token);
      router.push('/dashboard');
    } catch (err) {
      alert('Error al iniciar sesión: ' + err.message);
    }
    */
  };

  return (
    <div className={styles["login-page"]}>
      <div className={styles["login-overlay"]}></div>
      <div className={styles["login-container"]}>
        <h2>Iniciar sesión</h2>
        <p>Ingresa tu <b>usuario</b> y <b>contraseña</b> para poder ingresar al sistema</p>
        <form onSubmit={handleLogin}>
          <div>
            <label className={styles['login-subtitles']}>Usuario:</label><br />
            <input className={styles['login-subtitles']}
              type="text"
              value={user}
              onChange={e => setUser(e.target.value)}
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
        <p style={{marginTop: '1rem'}}>¿No tienes cuenta? <Link href="/registration"><b>Regístrate</b></Link></p>
      </div>
    </div>
  );
}
