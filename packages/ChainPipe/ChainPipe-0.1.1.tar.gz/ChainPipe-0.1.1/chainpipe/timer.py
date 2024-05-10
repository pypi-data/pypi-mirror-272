import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def start(self):
        self.start_time = time.time_ns()

    def stop(self):
        self.end_time = time.time_ns()

    def elapsed_ns(self):
        return self.end_time - self.start_time

    @staticmethod
    def format_time(nanoseconds):
        seconds = nanoseconds / 1_000_000_000
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{int(seconds)}s {milliseconds}ms"
