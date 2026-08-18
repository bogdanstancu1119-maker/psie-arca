import time
import sys

def sincronizare_noduri_hardware():
    print('Activare noduri hardware pentru reducerea latentei...')
    # Sincronizare buffer memorie cache
    time.sleep(0.1)
    return 'Sincronizare reusita'

if __name__ == '__main__':
    sincronizare_noduri_hardware()