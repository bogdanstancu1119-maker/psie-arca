import { validateAgency } from './psi-core';
const AGENTS = ['Telegram', 'Rander', 'Kimi'];
export function reconcileAgents(context) {
  return AGENTS.map(agent => {
    const metrics = context.getMetrics(agent);
    if (metrics.A < 0.7 || metrics.SDI > 0.7) {
      context.applyBackoff(agent);
      return { agent, status: 'recalibrating', mode: 'R_hat' };
    }
    return { agent, status: 'aligned', mode: 'active' };
  });
}
export function garbageCollect(nodes) {
  return nodes.filter(node => node.SDI < 0.7);
}