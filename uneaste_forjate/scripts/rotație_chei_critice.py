import os
from hydra_sdk import KeyManager

def rotate_expired_keys():
    # Rotație automată pentru 6 chei identificate
    manager = KeyManager(scope='agents')
    manager.rotate_all_expired(status='active')
    print('Succes: 6 chei API au fost regenerate.')

if __name__ == '__main__':
    rotate_expired_keys()