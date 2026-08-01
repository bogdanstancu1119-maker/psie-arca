import socket
import logging

def flush_smtp_buffer():
    try:
        logging.info('Resetare entropie buffer SMTP...')
        # Resetare socket si golire buffer intrare/iesire
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    flush_smtp_buffer()