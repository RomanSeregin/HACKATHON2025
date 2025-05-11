
"""
The delay class is created to incorporate delays during animations / any actions that may need artificial
delay to let the player see the event that has happened.
Simple class that keeps track of delays, optimizing and simplifying the delay creation experience.
"""
class Delay:

    def __init__(self):
        self.delays = {}
        self.executed = set()
        self.allDelays = set()

    def start(self, key, frameLimit):

        self.delays[key] = {"frameCounter": 0, "frameLimit": frameLimit, "active": True}
        self.allDelays.add(key)
        self.executed.discard(key)

    def stop(self, key):

        if key in self.delays:
            self.delays[key]["active"] = False

    def disable(self, key):

        self.delays.pop(key, None)
        self.executed.discard(key)

    def restart(self, key):

        if key in self.delays:
            self.delays[key]["frameCounter"] = 0
            self.delays[key]["active"] = True
            self.executed.discard(key)

    def updateLimit(self, key, newLimit):

        if key in self.delays:
            self.delays[key]["frameLimit"] = newLimit

    def resetOrStart(self, key, frameLimit):

        if key in self.delays:
            self.restart(key)
            self.updateLimit(key, frameLimit)
        else:
            self.start(key, frameLimit)

    def increment(self):

        for key, delay in self.delays.items():
            if delay["active"]:
                delay["frameCounter"] += 1

    def delayPersistent(self, key):

        if key in self.delays:
            return self.delays[key]["frameCounter"] >= self.delays[key]["frameLimit"]
        return key in self.allDelays

    def delayOnce(self, key):

        if key in self.delays and self.delays[key]["frameCounter"] >= self.delays[key]["frameLimit"]:
            if key not in self.executed:
                self.executed.add(key)
                return True
        return False