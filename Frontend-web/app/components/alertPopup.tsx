// src/components/AlertPopup.tsx
import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';

type AlertProps = {
  message: string;
  type?: 'success' | 'error' | 'info';
  onClose: () => void;
};

const AlertPopup: React.FC<AlertProps> = ({ message, type = 'info', onClose }) => {
  const colors = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -40 }}
        transition={{ duration: 0.3 }}
        className={`fixed top-5 right-5 z-50 text-white px-6 py-3 rounded-xl shadow-lg ${colors[type]}`}
      >
        <div className="flex items-center gap-2">
          <span>{message}</span>
          <button onClick={onClose} className="ml-4 text-white font-bold">×</button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export default AlertPopup;
