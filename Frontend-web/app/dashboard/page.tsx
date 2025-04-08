"use client";

import React, { useState } from "react";
import styles from "../style.module.css";
import Link from "next/link";

// Definición de tipos para resolver los errores de TypeScript
type DiseaseInfo = {
  title: string | React.ReactNode;
  emoji: string;
  description: React.ReactNode;
};

type DiseaseInfoMap = {
  [key: string]: DiseaseInfo;
};

// Tipo para las claves de enfermedades
type DiseaseKey =
  | "hipertension"
  | "infarto"
  | "insuficiencia"
  | "arritmias"
  | "arteriosclerosis";

export default function DashboardPage() {
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [selectedDisease, setSelectedDisease] = useState<DiseaseKey | null>(
    null
  );

  // Información de enfermedades con emojis añadidos
  const diseaseInfo: DiseaseInfoMap = {
    hipertension: {
      title: "🩸 Hipertensión Arterial",
      emoji: "🩸",
      description: (
        <div className="space-y-4">
          <p className="mb-2">
            <strong>Definición:</strong> La hipertensión arterial es una
            condición médica crónica caracterizada por la elevación persistente
            de la presión arterial en las arterias.
          </p>

          <div>
            <h4 className="font-bold mb-2">Valores de referencia:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Normal: &lt;120/80 mmHg</li>
              <li>Elevada: 120-129/&lt;80 mmHg</li>
              <li>Hipertensión Etapa 1: 130-139/80-89 mmHg</li>
              <li>Hipertensión Etapa 2: ≥140/90 mmHg</li>
              <li>Crisis hipertensiva: &gt;180/120 mmHg</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Síntomas:</h4>
            <p>Generalmente asintomática, pero puede presentar:</p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Dolor de cabeza intenso</li>
              <li>Visión borrosa</li>
              <li>Mareos</li>
              <li>Fatiga</li>
              <li>Dificultad respiratoria</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Factores de riesgo:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Edad avanzada</li>
              <li>Antecedentes familiares</li>
              <li>Sobrepeso y obesidad</li>
              <li>Consumo elevado de sodio</li>
              <li>Sedentarismo</li>
              <li>Consumo excesivo de alcohol</li>
              <li>Estrés crónico</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Tratamiento:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Cambios en el estilo de vida:</strong> Dieta baja en
                sodio, actividad física regular, pérdida de peso si es
                necesario.
              </li>
              <li>
                <strong>Farmacológico:</strong> Diuréticos, IECA, ARA-II,
                bloqueadores de canales de calcio, betabloqueadores.
              </li>
              <li>
                <strong>Monitoreo:</strong> Control periódico de la presión
                arterial.
              </li>
            </ul>
          </div>
        </div>
      ),
    },
    infarto: {
      title: "❤️‍🩹 Infarto al Miocardio",
      emoji: "❤️‍🩹",
      description: (
        <div className="space-y-4">
          <p className="mb-2">
            <strong>Definición:</strong> Un infarto de miocardio ocurre cuando
            el flujo sanguíneo que lleva oxígeno al músculo cardíaco se reduce o
            se bloquea completamente, causando daño al tejido cardíaco.
          </p>

          <div>
            <h4 className="font-bold mb-2">Causas principales:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                Aterosclerosis (acumulación de placa en las arterias coronarias)
              </li>
              <li>Trombosis coronaria (coágulo sanguíneo)</li>
              <li>
                Espasmo coronario (contracción súbita de una arteria coronaria)
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Síntomas:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Dolor o malestar en el pecho:</strong> Sensación de
                presión, opresión, dolor intenso o ardor
              </li>
              <li>
                Dolor que irradia a los brazos (especialmente el izquierdo),
                hombro, espalda, cuello, mandíbula o estómago
              </li>
              <li>Dificultad para respirar</li>
              <li>Sudoración fría y profusa</li>
              <li>Náuseas y vómitos</li>
              <li>Mareo o aturdimiento</li>
              <li>Fatiga inusual</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Factores de riesgo:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Edad (hombres &gt;45 años, mujeres &gt;55 años)</li>
              <li>Tabaquismo</li>
              <li>Hipertensión arterial</li>
              <li>Colesterol elevado</li>
              <li>Diabetes</li>
              <li>Obesidad</li>
              <li>Sedentarismo</li>
              <li>Antecedentes familiares</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Tratamiento:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Inmediato:</strong> Aspirina, terapia trombolítica,
                angioplastia coronaria
              </li>
              <li>
                <strong>Medicamentos:</strong> Antiagregantes plaquetarios,
                betabloqueadores, estatinas, IECA
              </li>
              <li>
                <strong>Procedimientos invasivos:</strong> Angioplastia con
                stent, cirugía de bypass coronario
              </li>
            </ul>
          </div>
        </div>
      ),
    },
    insuficiencia: {
      title: "💔 Insuficiencia Cardíaca",
      emoji: "💔",
      description: (
        <div className="space-y-4">
          <p className="mb-2">
            <strong>Definición:</strong> La insuficiencia cardíaca es una
            condición crónica en la cual el corazón no puede bombear suficiente
            sangre para satisfacer las necesidades del organismo.
          </p>

          <div>
            <h4 className="font-bold mb-2">Tipos:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Insuficiencia cardíaca sistólica:</strong> El corazón no
                se contrae con suficiente fuerza
              </li>
              <li>
                <strong>Insuficiencia cardíaca diastólica:</strong> El corazón
                no se llena adecuadamente de sangre
              </li>
              <li>
                <strong>Insuficiencia cardíaca derecha:</strong> El ventrículo
                derecho no funciona correctamente
              </li>
              <li>
                <strong>Insuficiencia cardíaca izquierda:</strong> El ventrículo
                izquierdo no funciona correctamente
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Síntomas:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Fatiga y debilidad</li>
              <li>Dificultad para respirar (disnea)</li>
              <li>Hinchazón (edema) en piernas, tobillos y pies</li>
              <li>Pulso irregular o acelerado</li>
              <li>Tos persistente con esputo blanco o rosado</li>
              <li>
                Aumento de la necesidad de orinar, especialmente por la noche
              </li>
              <li>Dificultad para concentrarse o mantenerse alerta</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Causas:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Enfermedad coronaria</li>
              <li>Infarto de miocardio previo</li>
              <li>Hipertensión arterial</li>
              <li>Valvulopatías</li>
              <li>Cardiomiopatías</li>
              <li>Cardiopatías congénitas</li>
              <li>Arritmias</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Tratamiento:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Medicamentos:</strong> IECA/ARA-II, betabloqueadores,
                diuréticos, digitálicos
              </li>
              <li>
                <strong>Dispositivos:</strong> Marcapasos, desfibriladores
                implantables, terapia de resincronización cardíaca
              </li>
              <li>
                <strong>Cirugía:</strong> Revascularización coronaria,
                reparación/reemplazo valvular, trasplante cardíaco
              </li>
              <li>
                <strong>Cambios en el estilo de vida:</strong> Restricción de
                sodio, control de líquidos, ejercicio apropiado, abandono del
                tabaco
              </li>
            </ul>
          </div>
        </div>
      ),
    },
    arritmias: {
      title: "⚡ Arritmias Cardíacas",
      emoji: "⚡",
      description: (
        <div className="space-y-4">
          <p className="mb-2">
            <strong>Definición:</strong> Las arritmias son alteraciones del
            ritmo cardíaco normal. Ocurren cuando los impulsos eléctricos que
            coordinan los latidos del corazón no funcionan adecuadamente.
          </p>

          <div>
            <h4 className="font-bold mb-2">Tipos principales:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Taquicardia:</strong> Ritmo cardíaco rápido (&gt;100
                latidos por minuto)
              </li>
              <li>
                <strong>Bradicardia:</strong> Ritmo cardíaco lento (&lt;60
                latidos por minuto)
              </li>
              <li>
                <strong>Fibrilación auricular:</strong> Latidos irregulares en
                las aurículas
              </li>
              <li>
                <strong>Fibrilación ventricular:</strong> Latidos rápidos e
                irregulares en los ventrículos
              </li>
              <li>
                <strong>Extrasístoles:</strong> Latidos prematuros o adicionales
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Síntomas:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                Palpitaciones (sensación de aleteo o golpeteo en el pecho)
              </li>
              <li>Latidos saltados o pausas</li>
              <li>Mareo o aturdimiento</li>
              <li>Desmayo (síncope)</li>
              <li>Fatiga</li>
              <li>Dificultad para respirar</li>
              <li>Dolor en el pecho</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Diagnóstico:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Electrocardiograma (ECG)</li>
              <li>Holter (monitoreo ECG por 24-48 horas)</li>
              <li>Monitor de eventos cardíacos</li>
              <li>Prueba de esfuerzo</li>
              <li>Ecocardiograma</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Tratamiento:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Medicamentos:</strong> Antiarrítmicos, betabloqueadores,
                anticoagulantes
              </li>
              <li>
                <strong>Cardioversión:</strong> Procedimiento para restaurar el
                ritmo normal
              </li>
              <li>
                <strong>Ablación por catéter:</strong> Destrucción del tejido
                cardíaco causante de la arritmia
              </li>
              <li>
                <strong>Marcapasos:</strong> Dispositivo para regular el ritmo
                cardíaco
              </li>
              <li>
                <strong>Desfibrilador:</strong> Dispositivo para corregir ritmos
                peligrosos
              </li>
            </ul>
          </div>
        </div>
      ),
    },
    arteriosclerosis: {
      title: "🧱 Arterioesclerosis",
      emoji: "🧱",
      description: (
        <div className="space-y-4">
          <p className="mb-2">
            <strong>Definición:</strong> La arteriosclerosis es el
            endurecimiento y pérdida de elasticidad de las paredes arteriales,
            generalmente causada por la acumulación de placas de grasa (ateroma)
            en el interior de las arterias.
          </p>

          <div>
            <h4 className="font-bold mb-2">Tipos:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Aterosclerosis:</strong> Acumulación de placa grasa en
                las arterias
              </li>
              <li>
                <strong>Esclerosis de Mönckeberg:</strong> Calcificación de la
                capa media arterial
              </li>
              <li>
                <strong>Arterioloesclerosis:</strong> Afecta a las arterias más
                pequeñas y arteriolas
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Síntomas:</h4>
            <p>
              Generalmente asintomática hasta etapas avanzadas, los síntomas
              dependen de las arterias afectadas:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Arterias coronarias:</strong> Angina de pecho, infarto
              </li>
              <li>
                <strong>Arterias cerebrales:</strong> ACV, AIT, deterioro
                cognitivo
              </li>
              <li>
                <strong>Arterias periféricas:</strong> Claudicación
                intermitente, dolor en extremidades
              </li>
              <li>
                <strong>Arterias renales:</strong> Hipertensión, insuficiencia
                renal
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Factores de riesgo:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Edad avanzada</li>
              <li>Tabaquismo</li>
              <li>Hipertensión arterial</li>
              <li>Colesterol elevado</li>
              <li>Diabetes</li>
              <li>Obesidad</li>
              <li>Sedentarismo</li>
              <li>Antecedentes familiares</li>
              <li>Dieta rica en grasas saturadas</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Diagnóstico:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Análisis de sangre (perfil lipídico)</li>
              <li>Ecografía Doppler</li>
              <li>Angiografía</li>
              <li>Tomografía computarizada</li>
              <li>Índice tobillo-brazo</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-2">Tratamiento:</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong>Cambios en el estilo de vida:</strong> Dieta saludable,
                ejercicio regular, abandono del tabaco
              </li>
              <li>
                <strong>Medicamentos:</strong> Estatinas, antiagregantes
                plaquetarios, antihipertensivos
              </li>
              <li>
                <strong>Procedimientos:</strong> Angioplastia con stent,
                endarterectomía, bypass
              </li>
            </ul>
          </div>
        </div>
      ),
    },
  };

  // Función para abrir el modal con la información de la enfermedad seleccionada
  const openDiseaseInfo = (disease: DiseaseKey) => {
    setSelectedDisease(disease);
    setIsModalOpen(true);
  };

  // Componente para el modal - Modificado con fondo blanco para mejor legibilidad
  const DiseaseModal = () => {
    if (!selectedDisease) return null;

    const disease = diseaseInfo[selectedDisease];

    return (
      <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
        <div className="bg-white rounded-lg shadow-lg w-11/12 max-w-3xl max-h-5/6 overflow-hidden flex flex-col">
          <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-blue-600 text-white">
            <h2 className="text-xl font-bold flex items-center">
              {disease.title}
            </h2>
            <button
              onClick={() => setIsModalOpen(false)}
              className="text-white hover:text-gray-200"
            >
              <span className="text-2xl">&times;</span>
            </button>
          </div>
          <div className="p-6 overflow-y-auto text-gray-800">
            {disease.description}
          </div>
          <div className="p-4 border-t border-gray-200 flex justify-end bg-gray-100">
            <button
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={styles["home-container"]}>
      <div className={styles["container-box"]}>
        <h2>👋 Bienvenido al Sistema Inteligente de Salud</h2>
        <p>
          Este sistema está diseñado para ayudarte a comprender mejor el
          funcionamiento del cuerpo humano, especialmente el{" "}
          <strong>sistema circulatorio</strong> ❤️.
        </p>

        <div style={{ marginTop: "1.5rem", textAlign: "left" }}>
          <h3>📋 Principales enfermedades del sistema circulatorio:</h3>
          <ul className="disease-list space-y-2">
            <li
              onClick={() => openDiseaseInfo("hipertension")}
              className="cursor-pointer hover:text-blue-600 hover:underline flex items-center"
            >
              <span className="mr-2">🩸</span>
              <span>
                <strong>Hipertensión arterial:</strong> Presión elevada de forma
                continua.
              </span>
            </li>
            <li
              onClick={() => openDiseaseInfo("infarto")}
              className="cursor-pointer hover:text-blue-600 hover:underline flex items-center"
            >
              <span className="mr-2">❤️‍🩹</span>
              <span>
                <strong>Infarto al miocardio:</strong> Bloqueo del flujo
                sanguíneo al corazón.
              </span>
            </li>
            <li
              onClick={() => openDiseaseInfo("insuficiencia")}
              className="cursor-pointer hover:text-blue-600 hover:underline flex items-center"
            >
              <span className="mr-2">💔</span>
              <span>
                <strong>Insuficiencia cardíaca:</strong> El corazón no bombea
                sangre eficientemente.
              </span>
            </li>
            <li
              onClick={() => openDiseaseInfo("arritmias")}
              className="cursor-pointer hover:text-blue-600 hover:underline flex items-center"
            >
              <span className="mr-2">⚡</span>
              <span>
                <strong>Arritmias:</strong> Latidos irregulares del corazón.
              </span>
            </li>
            <li
              onClick={() => openDiseaseInfo("arteriosclerosis")}
              className="cursor-pointer hover:text-blue-600 hover:underline flex items-center"
            >
              <span className="mr-2">🧱</span>
              <span>
                <strong>Arteriosclerosis:</strong> Endurecimiento de arterias
                por placas de grasa.
              </span>
            </li>
          </ul>
          <p className="text-sm text-gray-600 mt-2 italic">
            (Haz clic en cualquier enfermedad para ver más información)
          </p>
        </div>

        <div style={{ marginTop: "2rem" }}>
          <p>
            <strong>Selecciona una opción del menú:</strong>
          </p>

          <br />
          <Link href="/dashboard/quotes">
            <button className={styles["login-button"]}>📅 Reservar Cita</button>
          </Link>
          <br />
          <Link href="/dashboard/history">
            <button className={styles["login-button"]}>📋 Historial</button>
          </Link>
        </div>
      </div>

      {/* Modal para mostrar información de enfermedades */}
      {isModalOpen && <DiseaseModal />}
    </div>
  );
}
