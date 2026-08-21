import os
from datetime import datetime

def initialize_stream():
    print(f'Sincronizare activata la {datetime.now().isoformat()}')
    # Activare flux de date pentru API-urile detectate
    return True

if __name__ == '__main__':
    initialize_stream()