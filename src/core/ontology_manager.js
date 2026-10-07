import { isolationModule, autopoiesis } from './core/psie_kernel';

const AGENTS = ['Rander', 'Kimi'];

export const manageAgentOntology = (systemState) => {
  return AGENTS.map(agent => {
    const agentStatus = systemState.agents[agent];
    if (agentStatus.A < 0.2) {
      console.warn(`[PSIE-KERNEL] Initiating forced recalibration for ${agent}`);
      const recalibratedAgent = autopoiesis.recalibrate(agentStatus);
      if (recalibratedAgent.isAligned) {
        return { ...recalibratedAgent, status: 'INTEGRATED' };
      } else {
        return { ...isolationModule.isolate(agentStatus), status: 'ARCHIVED' };
      }
    }
    return agentStatus;
  });
};

export default manageAgentOntology;