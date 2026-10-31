import { useState, useEffect } from 'react';

export const useAgentHydraState = (key, initialValue) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    const persistToCloud = async (data) => {
      try {
        await fetch('/api/sync-agent-state', { method: 'POST', body: JSON.stringify({ key, data }) });
      } catch (err) {
        console.error('Cloud sync failed, keeping local backup', err);
      }
    };
    localStorage.setItem(key, JSON.stringify(state));
    persistToCloud(state);
  }, [key, state]);

  return [state, setState];
};