import json
from datetime import datetime

def rezuma_flux(date_in):
    coerenta = 0.62
    prag = 0.80
    return f'Sincronizare activată. Coerență: {coerenta}. Reducere încărcare la {prag*100}% prin abstractizarea semantică a nodurilor secundare.'

print(rezuma_flux('6a8619bcdd09e5c1d0a0541b'))