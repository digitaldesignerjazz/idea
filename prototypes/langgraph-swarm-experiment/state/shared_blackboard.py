# Simple in-memory shared blackboard for the swarm

class SharedBlackboard:
    def __init__(self):
        self.data = {}

    def post(self, key: str, value: any):
        self.data[key] = value

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def get_all(self):
        return self.data.copy()