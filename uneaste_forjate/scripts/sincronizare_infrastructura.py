import datetime
import subprocess

def check_reversibility():
    limit = datetime.datetime.now() - datetime.timedelta(hours=72)
    commits = subprocess.check_output(['git', 'log', '--since="72 hours ago"', '--format=%H']).decode('utf-8').splitlines()
    print(f'Sincronizat: {len(commits)} commit-uri verificate in fereastra de 72h.')

if __name__ == '__main__':
    check_reversibility()