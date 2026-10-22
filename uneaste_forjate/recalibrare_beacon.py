import logging

def recalibrare_traiectorie(j_val, sdi_val):
    # Corecție pentru deviația negativă critică
    if j_val < -30000:
        logging.info('Aplicare vector de compensare 30145')
        return j_val + 30145
    return j_val

if __name__ == '__main__':
    print(recalibrare_traiectorie(-30145, 0.27))