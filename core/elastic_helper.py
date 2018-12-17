from threading import Thread
import time
import json
import redis
import requests
import datetime


redis_client = redis.Redis()


def worker():
    while True:
        if redis_client.llen('ics') == 0:
            time.sleep(2)
            continue

        record = redis_client.lpop('ics')
        record = json.loads(record)

        data = record['data']
        print(data[record['data'].keys()[0]]['status'])
        if data[record['data'].keys()[0]]['status'] == 'success':
            record['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            resp = requests.post('http://localhost:9200/ics/packet', json=record)
            print(resp.status_code)


t = Thread(target=worker)
t.start()
t.join()
