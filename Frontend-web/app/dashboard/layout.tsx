import Link from 'next/link';
import styles from '../style.module.css';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav className={styles.navbar}>
        <Link href="/dashboard">Inicio</Link>
        <Link href="/dashboard/information">Información</Link>
        <Link href="/dashboard/quotes">Citas</Link>
        <Link href="/dashboard/history">Historial</Link>
      </nav>
      {children}
    </div>
  );
}
