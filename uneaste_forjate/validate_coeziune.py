import sys
def valideaza_input(payload):
    if 'validare de coeziune' not in payload:
        raise ValueError('Aliniere esuata: Frictiune controlata necesara.')
    return True

if __name__ == '__main__':
    print('Validare coeziune activa pentru strat beacon_critc.')