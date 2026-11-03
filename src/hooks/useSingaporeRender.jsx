import { useState, useEffect } from 'react';

export const useSingaporeRender = (initialState) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem('singapore_state');
    return saved ? JSON.parse(saved) : initialState;
  });

  useEffect(() => {
    const syncState = async () => {
      try {
        await fetch('/api/sync', { method: 'POST', body: JSON.stringify(state) });
        localStorage.setItem('singapore_state', JSON.stringify(state));
      } catch (e) {
        console.error('Sync failure', e);
      }
    };
    syncState();
  }, [state]);

  return [state, setState];
};