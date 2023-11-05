import requests

def gen_logs():
    r = requests.get('http://5.53.124.214:8080/logs')

    file = 'logs.log'

    f = open(f'./{file}', 'w')
    f.write(r.text)
    f.close

    return file