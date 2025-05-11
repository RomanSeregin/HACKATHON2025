# A separate brach of delay with less functions to handle animations
class EntityDelay:
    def __init__(self):
        self.delays = {}
        self.executed = set()

    def start(self, key, frameLimit):
        self.delays[key] = {"frameCounter": 0, "frameLimit": frameLimit}
        if key in self.executed:
            self.executed.remove(key)

    def stop(self, key):
        if key in self.delays:
            del self.delays[key]

    def increment(self):
        for key in self.delays:
            self.delays[key]["frameCounter"] += 1

    def delayOnce(self, key):
        if key in self.delays and self.delays[key]["frameCounter"] >= self.delays[key]["frameLimit"]:
            if key not in self.executed:
                self.executed.add(key)
                return True
        return False