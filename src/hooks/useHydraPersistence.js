import { useState, useEffect } from 'react';

const useHydraPersistence = (key, initialValue) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    const saveToRemote = async () => {
      try {
        await fetch('/api/persistence/sync', {
          method: 'POST',
          body: JSON.stringify({ key, value: state }),
          headers: { 'Content-Type': 'application/json' }
        });
        localStorage.setItem(key, JSON.stringify(state));
      } catch (e) {
        console.error('Eroare persistență:', e);
      }
    };
    saveToRemote();
  }, [key, state]);

  return [state, setState];
};

export default useHydraPersistence;