import datetime

def check_commit_window(last_commit_date):
    current_date = datetime.datetime.now()
    delta = current_date - last_commit_date
    if delta.total_seconds() < 259200:
        raise Exception('Violare fereastra ontologica: Commit-ul trebuie sa astepte 72h.')
    return True