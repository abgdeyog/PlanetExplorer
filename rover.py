from environment import Environment
import numpy as np
import random


class Rover:
    def __init__(self, id, initial_position, env: Environment, bounds):
        self.bounds = bounds
        self.position = initial_position
        self.id = id
        self.env = env
        self.info = self.env.get_info(self.position)
        self.best_position = np.array(self.position)
        self.best_info = self.env.get_info(self.position)
        self.global_best_info = self.best_info
        self.global_best_position = np.array(self.best_position)
        self.omega = 0.05
        self.omegap = 0.05
        self.omegag = 0.5
        self.v = np.array([random.random(), random.random()])

    def move(self, vector, time):
        self.position += vector*time

    def update_info(self):
        self.info = self.env.get_info(self.position)
        if self.info > self.best_info:
            self.best_info = self.info

    def get_position(self):
        return self.position

    def update_global_best(self, satellites):
        for satellite in satellites:
            if satellite.get_info()[1] > self.global_best_info:
                self.global_best_info = satellite.get_info()[1]
                self.global_best_position = satellite.get_info()[0]

    def get_best_info(self):
        return [self.best_position, self.best_info]

    def step(self):
        rp = random.random()
        rg = random.random()
        self.v = self.omega * self.v + self.omegap * rp * (self.best_position - self.position)\
                 + self.omegag * rg * (self.global_best_position - self.position)
        self.move(self.v, 0.05)
