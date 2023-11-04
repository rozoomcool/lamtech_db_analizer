import requests
import json


def crush_db():
    return 1

def restart_db():
    r = requests.get('http://5.53.124.214:8080/restartdb')

    return r.status_code

# r = requests.post('http://5.53.124.214:8080/bench', json={"scaleFactor": "10", "clients": "10", "threads": "2", "seconds": "10"}, headers={"Content-Type": "application/json"})
# per_r = requests.get('http://5.53.124.214:8080/performance', headers={"Content-Type": "application/json"})



# print(per_r.text)

# result = json.loads(r.text)['output'].split("\n").pop(-1)
# print(result)
# print(r.text)
