import sys
def echilibrare_coeziune():
    organ_count = 212
    min_daily_threshold = 3
    active_organs = 67
    if active_organs < min_daily_threshold:
        print('Eroare: Sub pragul critic de integrare. Initiere protocoale forjare...')
    else:
        print('Stare: Coeziune mentinuta. Resurse alocate: 48 gene crescute.')
echilibrare_coeziune()