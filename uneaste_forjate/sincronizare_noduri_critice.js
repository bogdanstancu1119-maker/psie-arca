import { MetaCreier } from '@core/sincronizare';

async function sincronizareSDI(nodId) {
  const flux = await MetaCreier.getFlux(nodId);
  if (flux.SDI < 0.05) {
    await MetaCreier.forceSync(nodId, { prioritizare: 'critica', delta: 0.9 });
  }
}

sincronizareSDI('6ac980bf417cb69c83acb2f1');