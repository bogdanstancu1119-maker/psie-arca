import logging
from hydra_core import sync_engine

def recalibrare_coerenta():
    logging.info('Initiere protocol consolidare 70% pentru beacon_critc')
    sync_engine.force_sync(target_threshold=0.70)
    sync_engine.verify_integrity()

if __name__ == '__main__':
    recalibrare_coerenta()