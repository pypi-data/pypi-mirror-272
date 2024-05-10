import time

import httpx


class Heartbeat:
    def __init__(self, db_url):
        self.db_url = db_url

    def heartbeat(self):
        while True:
            try:
                resp = httpx.get(self.db_url)
                if resp.status_code == 200:
                    print('Heartbeat success')
            except Exception as e:
                print(e)
            time.sleep(10)
