import { useState, useEffect } from 'react';

export const useRenderPersistence = (key, initialValue) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    const syncState = () => {
      localStorage.setItem(key, JSON.stringify(state));
    };
    syncState();
  }, [state, key]);

  return [state, setState];
};

export const RenderSingapore = ({ config }) => {
  const [persistence, setPersistence] = useRenderPersistence('render_sg_state', config);
  return <div data-state={JSON.stringify(persistence)}>Render Active</div>;
};