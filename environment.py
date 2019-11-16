
class Environment:
    def __init__(self, map, communication_distance):
        self.map = map
        self.communication_distance = communication_distance

    def get_info(self, position):
        return self.map(position[0], position[1])

    def count_distance(self, position_a, position_b):
        return (position_a[0] - position_b[0])**2 + (position_a[1] - position_b[1])**2

    def is_reachable(self, position_a, position_b):
        return self.count_distance(position_a, position_b) < self.communication_distance**2

