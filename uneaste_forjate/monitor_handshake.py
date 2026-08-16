import requests
import time
def verify_handshake(api_url):
    try:
        response = requests.get(f'{api_url}/health')
        return response.status_code == 200
    except Exception:
        return False
while True:
    if not verify_handshake('https://api.hydra.internal'):
        print('Handshake failure detected')
    time.sleep(60)