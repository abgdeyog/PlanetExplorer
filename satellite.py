import numpy as np


class Satellite:
    def __init__(self, id, initial_position, movement_vector, bounds):
        self.bounds = bounds
        self.id = id
        self.position = np.array(initial_position)
        self.rovers_info = []
        self.vector = np.array(movement_vector)
        self.best_position = [0, 0]
        self.best_value = -1

    def move(self, vector, time):
        self.position += vector * time
        if self.position[0] < self.bounds[0][0]:
            self.position[0] = self.position[0] = self.bounds[0][0] - self.position[0]
        if self.position[0] > self.bounds[0][1]:
            self.position[0] = self.position[0] = self.position[0] - self.bounds[0][1]

        if self.position[1] < self.bounds[1][0]:
            self.position[1] = self.position[1] = self.bounds[1][0] - self.position[1]
        if self.position[1] > self.bounds[1][1]:
            self.position[1] = self.position[1] = self.position[1] - self.bounds[1][1]

    def sync_with_rovers(self, rovers_list):
        rovers_infos = [rover.get_best_info() for rover in rovers_list]
        for rover_info in rovers_infos:
            # print(rover_info)
            if rover_info[1] > self.best_value:
                self.best_value = rover_info[1]
                self.best_position = rover_info[0]
        # print("-----------------------------")
        # print(self.get_info())
        # print("-----------------------------")

    def get_position(self):
        return self.position

    def get_info(self):
        return [self.best_position, self.best_value]

    def sync_with_satellite(self, other_satellite_best_info):
        if other_satellite_best_info[1] > self.best_value:
            self.best_value = other_satellite_best_info[1]
            self.best_position = other_satellite_best_info[0]

    def step(self):
        self.move(self.vector, 1)