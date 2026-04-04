
class FakeGeneration:

    def __init__(self):
        self.recorded_output = []

    def end(self, output, latency=None):
        self.recorded_output = output
        