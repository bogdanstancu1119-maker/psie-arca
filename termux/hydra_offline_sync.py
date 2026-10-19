import json, time, os, requests, subprocess

WEBHOOK_URL = 'https://example.com/base44_endpoint'
CACHE_FILE = 'hydra_cache.json'
BUFFER_FILE = 'hydra_offline_buffer.jsonl'

def check_internet():
    return subprocess.call(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.DEVNULL) == 0

def run_psi_rules(cache):
    decision = {'ts': time.time(), 'sdi': 0.5, 'action': 'autonomous_check'}
    return decision

def sync_buffer():
    if os.path.exists(BUFFER_FILE) and check_internet():
        with open(BUFFER_FILE, 'r') as f:
            data = [json.loads(line) for line in f]
        try:
            requests.post(WEBHOOK_URL, json=data)
            os.remove(BUFFER_FILE)
        except: pass

while True:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        if not check_internet():
            entry = run_psi_rules(cache)
            with open(BUFFER_FILE, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        else:
            sync_buffer()
    time.sleep(300)