import { useState, useEffect, useCallback } from 'react';

const HydraRezolvaProblema = ({ context, onIntegrate }) => {
  const [state, setState] = useState({ sdi: 0.99, phase: 'decoupled' });
  const [history, setHistory] = useState([]);

  const recycleMorphology = useCallback((fragment) => {
    setHistory((prev) => [...prev, { ...fragment, timestamp: Date.now() }]);
    return { sdi: 0.1, phase: 'aligned' };
  }, []);

  useEffect(() => {
    if (state.sdi > 0.9) {
      const newState = recycleMorphology(state);
      setState(newState);
      onIntegrate?.(newState);
    }
  }, [state.sdi, recycleMorphology, onIntegrate]);

  return { state, history };
};