import { throttle, synchronizeAgents } from './engine/psieCore';
const AGENTS = ['Maritaca-Sabia', 'Zhipu-GLM'];
export const recalibrateAgents = async () => {
  const status = await synchronizeAgents(AGENTS);
  if (status.sdi > 0.7) {
    throttle(AGENTS, 0.7);
    await Promise.all(AGENTS.map(agent => agent.forceAlignment({ targetTheta: 0 })));
  }
  return { status: 'synchronized', entropy: 'minimized' };
};
export default { recalibrateAgents };