import threading
import time


class BackgroundProcess:
    def __init__(self, on_update, interval=1000*60):
        self.on_update = on_update
        self.interval = interval
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    async def run(self):
        while True:
            await self.update()
            time.sleep(self.interval)

    async def update(self):
        await self.on_update()
