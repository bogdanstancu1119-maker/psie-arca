import os

def sync_infrastructure_free_tier():
    config = {'mode': 'free', 'priority': 'optimized'}
    with open('infra_config.json', 'w') as f:
        f.write(str(config))
    print('Infrastructure synced to free-tier provider.')

sync_infrastructure_free_tier()