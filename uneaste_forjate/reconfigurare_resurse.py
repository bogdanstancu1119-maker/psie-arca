import os

def switch_to_free_tier():
    # Sincronizare parametri beacon_critc pentru resurse gratuite
    config = {'tier': 'free', 'budget_limit': 0, 'status': 'optimized'}
    return config

if __name__ == '__main__':
    print('Migrare catre resurse gratuite activata.')