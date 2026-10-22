import logging

def audit_edge_sync():
    noduri = ['edge_01', 'edge_02', 'edge_03']
    for nod in noduri:
        status = 'reset_buffer'
        logging.info(f'Resetare buffer pentru {nod}: status={status}')

if __name__ == '__main__':
    audit_edge_sync()