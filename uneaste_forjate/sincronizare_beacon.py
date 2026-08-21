import logging
logging.basicConfig(level=logging.INFO)
def executa_protocol_suprapunere():
    coeziune_curenta = 0.62
    if coeziune_curenta < 0.8:
        logging.info('Initiere Protocol de Suprapunere: Realiniere straturi beacon_critc...')
        return True
    return False
executa_protocol_suprapunere()