import { api, ui } from 'hydra-core';

async function resolveSyncLoop() {
  const status = await api.check_state('6a6fcc735e466f7ca78af843');
  if (status === 'nou') {
    await ui.sync_wait_mode('enabled');
    await api.patch_state('6a6fcc735e466f7ca78af843', { status: 'rezolvat', sync_lock: false });
  }
}

resolveSyncLoop();