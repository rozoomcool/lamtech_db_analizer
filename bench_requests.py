import requests
import json

def restart_db():
    r = requests.get('http://5.53.124.214:8080/restartdb')

    return r.status_code

# TODO: one test with specific parametrs

def easy_test():
    r = requests.post('http://5.53.124.214:8080/bench', 
                      json={
                          "scaleFactor": "1", 
                          "clients": "1", 
                          "threads": "1", 
                          "seconds": "1"
                          })

    data = json.loads(r.text)

    return {"status": r.status_code, "data": data}

def hard_test():
    r = requests.post('http://5.53.124.214:8080/bench', json={"scaleFactor": "200", "clients": "200", "threads": "2", "seconds": "30"}, headers={"Content-Type": "application/json"})

    return {"status": r.status_code, "body": r.text}

def crush_db():
    r = requests.get('http://5.53.124.214:8080/killdb')

    return r.status_code

