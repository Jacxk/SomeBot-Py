import threading


class SetInterval:
    def __init__(self, time, func):
        self.time = time
        self.func = func
        self.onend = threading.Event()
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        while not self.onend.wait(self.time):
            self.func()

    def stop(self):
        self.onend.set()
