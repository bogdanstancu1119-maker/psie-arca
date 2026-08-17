import json
import zlib
import os

def comprima_si_arhiveaza(memorii_raw):
    date_binare = json.dumps(memorii_raw).encode('utf-8')
    date_comprimate = zlib.compress(date_binare)
    with open('arhiva_nucleu_compressed.bin', 'wb') as f:
        f.write(date_comprimate)
    return 'Arhivare finalizata cu succes'

# Executare rutina pentru 344 memorii
comprima_si_arhiveaza({'stare': 'compresie_nucleu', 'count': 344})