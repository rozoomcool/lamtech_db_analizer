import requests

def backup_db():
    r = requests.post('http://5.53.124.214:8080/backup')

    return r.text

def restore_db():
    r = requests.post('http://5.53.124.214:8080/restore')

    return r.text