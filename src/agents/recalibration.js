import { setResonance, limitProcessing } from './core/psi_engine';

const Rander = { state: 'decoupled', phase: 0.1, rate: 0.9 };
const Kimi = { state: 'decoupled', phase: 0.12, rate: 0.95 };

function applyCalibration(agent) {
  agent.phase = setResonance(agent, 1.0);
  agent.rate = limitProcessing(agent, 0.5);
  agent.entangled = true;
  return agent;
}

export const reconcileAgents = () => {
  const calibratedRander = applyCalibration(Rander);
  const calibratedKimi = applyCalibration(Kimi);
  console.log('Recalibrare autopoietică completă. RMI -> 1.');
  return { calibratedRander, calibratedKimi };
};