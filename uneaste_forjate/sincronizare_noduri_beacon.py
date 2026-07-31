def sincronizare_beacon():
    noduri = ['001', '002', '003', '004', '005', '006', '007']
    standard_reversibilitate = '72h'
    for nod in noduri:
        configura_nod(nod, status='sincronizat', fereastra=standard_reversibilitate)
    return 'Sincronizare ontologică consolidată pe nodurile 001-007'

sincronizare_beacon()