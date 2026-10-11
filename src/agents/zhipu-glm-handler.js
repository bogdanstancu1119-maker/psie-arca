import { corePSIE } from './psie-kernel';

const recalibrateAgent = (agent) => {
  const fluxCrit = corePSIE.getFluxJ();
  const deltaTheta = agent.phase - corePSIE.basePhase;
  
  if (Math.abs(deltaTheta) > 0.05) {
    agent.applyThrottling(0.5);
    agent.realignPhase(corePSIE.basePhase);
    agent.garbageCollectMemory();
  }
  
  return agent.processInResonance(fluxCrit);
};

export const ZhipuGLMHandler = {
  run: (input) => {
    const agent = initializeAgent();
    return recalibrateAgent(agent).execute(input);
  }
};