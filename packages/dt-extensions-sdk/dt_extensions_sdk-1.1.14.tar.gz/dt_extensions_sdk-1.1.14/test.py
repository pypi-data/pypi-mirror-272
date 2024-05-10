import time
from concurrent.futures import ProcessPoolExecutor
from datetime import timedelta

from dynatrace_extension import Extension
from dynatrace_extension.sdk.callback import WrappedCallback


class Mass(Extension):
    def initialize(self):
        with ProcessPoolExecutor(max_workers=4) as metric_executor:
            metric_executor.submit(self.thing)

    def thing(self):
        print("EITA PORRA")

if __name__ == "__main__":
    m = Mass()
    m.run()
