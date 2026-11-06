import { useState, useEffect, useCallback } from 'react';

export const useHydraWorkerState = (agentId, initialState) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem(`hydra-agent-${agentId}`);
    return saved ? JSON.parse(saved) : initialState;
  });

  const syncToCloud = useCallback(async (newState) => {
    try {
      await fetch('/api/hydra/sync', {
        method: 'POST',
        body: JSON.stringify({ agentId, data: newState })
      });
    } catch (e) {
      console.error('Sync failed, relying on local backup', e);
    }
  }, [agentId]);

  useEffect(() => {
    localStorage.setItem(`hydra-agent-${agentId}`, JSON.stringify(state));
    syncToCloud(state);
  }, [state, agentId, syncToCloud]);

  return [state, setState];
};