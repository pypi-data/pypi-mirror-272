import signal
import time

from avocado import Test


class Ignore(Test):
    def test(self):
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        time.sleep(30)
