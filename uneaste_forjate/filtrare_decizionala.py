import json
from datetime import datetime

def filtrare_flux_informational(payload_input):
    # Reducerea obezitatii informationale prin eliminarea zgomotului
    threshold = 0.7
    if payload_input.get('relevanta', 0) < threshold:
        return 'arhivat_in_r2'
    return 'procesat_prioritar'

# Sincronizare beacon_critc
config = {'status': 'optimizat', 'timestamp': str(datetime.now())}
print(f'Sincronizare completă: {config}')