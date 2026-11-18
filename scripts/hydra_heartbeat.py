import json
import datetime
from pathlib import Path

def run_heartbeat():
    file_path = Path('dovada_executie.json')
    data = {'contor': 0}
    if file_path.exists():
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except:
            pass
    data['contor'] += 1
    data['timestamp_utc'] = datetime.datetime.utcnow().isoformat()
    data['mesaj'] = 'Execuție reală independentă de Base44 — platformă proprie GitHub Actions'
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Heartbeat confirmat: {data}')

if __name__ == '__main__':
    run_heartbeat()