import { useState, useEffect } from 'react';

export const useAgentState = (agentId) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem(`agent_state_${agentId}`);
    return saved ? JSON.parse(saved) : { identity: 'stable', context: null };
  });

  useEffect(() => {
    localStorage.setItem(`agent_state_${agentId}`, JSON.stringify(state));
  }, [state, agentId]);

  return [state, setState];
};

export const RenderSingaporeAgent = () => {
  const [state, setState] = useAgentState('singapore_01');
  return <div>Agent Status: {state.identity}</div>;
};