'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import styles from '../style.module.css';

export default function LoginPage() {
  const router = useRouter();

  const [user, setUser] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();
      formData.append('username', user);
      formData.append('password', password);

      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Credenciales incorrectas');
      }

      const data = await res.json();
      const token = data.access_token;
      console.log('Token recibido:', token);

      // Guardar el token en localStorage
      localStorage.setItem('token', token);

      // Obtener los datos del usuario
      const userRes = await fetch('http://localhost:8000/usuario', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!userRes.ok) {
        throw new Error('No se pudo obtener la información del usuario');
      }

      const userData = await userRes.json();
      console.log('Usuario logueado:', userData);

      // Guardar el ID del usuario en localStorage
      localStorage.setItem('user_id', userData.id);

      alert('Inicio de sesión exitoso');
      router.push('/dashboard');
    } catch (err: any) {
      alert('Error al iniciar sesión: ' + err.message);
    }
  };

  return (
    <div className={styles["login-page"]}>
      <div className={styles["login-overlay"]}></div>
      <div className={styles["login-container"]}>
        <h2>Iniciar sesión</h2>
        <p>Ingresa tu <b>usuario</b> y <b>contraseña</b> para poder ingresar al sistema</p>
        <form onSubmit={handleLogin}>
          <div className={styles['container-label']}>
            <label className={styles['login-subtitles']}>Usuario:</label><br />
            <input
              className={styles['login-subtitles']}
              type="text"
              value={user}
              onChange={e => setUser(e.target.value)}
              required
            />
          </div>
          <div className={styles['container-label']}>
            <label className={styles['login-subtitles']}>Contraseña:</label><br />
            <input
              className={styles['login-subtitles']}
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Iniciar sesión</button>
        </form>
        <p style={{ marginTop: '1rem' }}>
          ¿No tienes cuenta? <Link href="/registration"><b>Regístrate</b></Link>
        </p>
      </div>
    </div>
  );
}
