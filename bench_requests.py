import requests
import json


def crush_db():
    return 1

def restart_db():
    r = requests.get('http://5.53.124.214:8080/restartdb')

    return r.status_code

def easy_test():
    r = requests.post('http://5.53.124.214:8080/bench', json={"scaleFactor": "10", "clients": "10", "threads": "2", "seconds": "30"}, headers={"Content-Type": "application/json"})

    return {"status": r.status_code, "body": r.text}
def hard_test():
    r = requests.post('http://5.53.124.214:8080/bench', json={"scaleFactor": "200", "clients": "200", "threads": "2", "seconds": "30"}, headers={"Content-Type": "application/json"})

    return {"status": r.status_code, "body": r.text}

def crush_db():
    r = requests.get('http://5.53.124.214:8080/killdb')

    return r.status_code

