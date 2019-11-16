from satellite import Satellite
from rover import Rover
from environment import Environment
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import pickle
import random


def surface_characteristic(position_x, position_y):
    return gaussian2d(position_x/10, 80, 40, position_y/10, 40, 40) +\
           0.05 * gaussian2d(position_x/10, 60, 5, position_y/10, 70, 5)
    #return gaussian(position_x, 5, 4) + gaussian(position_y, 3, 2)


def gaussian2d(x, x0, sigx, y, y0, sigy):
    return np.exp(-(np.power(x - x0, 2.) / (2 * np.power(sigx, 2.))
                    + np.power(y - y0, 2.) / (2 * np.power(sigy, 2.))))


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


count_map = False
number_of_rovers = 30

matrix = np.zeros((1000, 1000))

if count_map:
    for x in range(1000):
        for y in range(1000):
            matrix[y][x] = surface_characteristic(x, y)
    map_file = open("map.p", "wb+")
    pickle.dump(matrix, map_file)
else:
    map_file = open("map.p", "rb")
    matrix = pickle.load(map_file)


def update_image(satellites, rovers, ax, rover_color='r', satellite_color='g'):
    for rover in rovers:
        circle = Circle(rover.get_position(), 10, color=rover_color)
        ax.add_patch(circle)
    for satellite in satellites:
        circle = Circle(satellite.get_position(), 20, color=satellite_color)
        ax.add_patch(circle)

history = []
def save_positions(satellites, rovers):
    for rover in rovers:
        history.append(rover.get_position())
    for satellite in satellites:
        history.append(satellite.get_position())


# initialize the game
environment = Environment(surface_characteristic, 500)
satellite_1 = Satellite(1, [300, 500], [50, 0], [[-1000, 2000], [-1000, 2000]])
satellite_2 = Satellite(2, [400, 1200], [0, 60], [[-1000, 2000], [-1000, 2000]])
rovers = []

fig, ax = plt.subplots(1)
ax.set_aspect('equal')
ax.imshow(matrix)

for rover_id in range(number_of_rovers):
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    rovers.append(Rover(rover_id, [x, y], environment, [[0, 1000], [0, 1000]]))

update_image([satellite_1, satellite_2], rovers, ax)
image_count = 0
images_dir = 'images'
plt.savefig(images_dir + '/image' + ''.join(['0' for i in range(4 - len(str(image_count)))]) + str(image_count))
image_count += 1
plt.close()

number_of_iterations = 300

for i in range(number_of_iterations):
    # fig, ax = plt.subplots(1)
    # ax.set_aspect('equal')
    # ax.imshow(matrix)
    reachable_rovers_to_satellite_1 = \
        [rover for rover in rovers
         if environment.is_reachable(satellite_1.get_position(), rover.get_position())]
    satellite_1.sync_with_rovers(reachable_rovers_to_satellite_1)
    # update_image([satellite_1], reachable_rovers_to_satellite_1, ax, rover_color='b')
    # plt.show()
    #
    # fig, ax = plt.subplots(1)
    # ax.set_aspect('equal')
    # ax.imshow(matrix)
    reachable_rovers_to_satellite_2 = \
        [rover for rover in rovers
         if environment.is_reachable(satellite_2.get_position(), rover.get_position())]
    satellite_2.sync_with_rovers(reachable_rovers_to_satellite_2)
    # update_image([satellite_2], reachable_rovers_to_satellite_2, ax, rover_color='b')
    # plt.show()
    satellite_1_info = satellite_1.get_info()
    satellite_2_info = satellite_2.get_info()
    satellite_1.sync_with_satellite(satellite_2_info)
    satellite_2.sync_with_satellite(satellite_1_info)
    satellite_1.step()
    satellite_2.step()
    # print("------------------------")
    # print(satellite_1.get_info())
    # fig, ax = plt.subplots(1)
    # ax.set_aspect('equal')
    # ax.imshow(matrix)
    # circle = Circle(satellite_1.get_info()[0], 10, color='b')
    # ax.add_patch(circle)
    # plt.show()
    # fig, ax = plt.subplots(1)
    # ax.set_aspect('equal')
    # ax.imshow(matrix)
    # circle = Circle(satellite_2.get_info()[0], 10, color='b')
    # ax.add_patch(circle)
    # plt.show()
    for rover in rovers:
        rover.update_global_best([satellite_1, satellite_2])
        rover.step()
    # print(len(reachable_rovers_to_satellite_1))

    # ax2.imshow(matrix)
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    ax.imshow(matrix)
    update_image([satellite_1, satellite_2], rovers, ax)
    save_positions([satellite_1, satellite_2], rovers)
    plt.savefig(images_dir + '/image' + ''.join(['0' for i in range(4 - len(str(image_count)))]) + str(image_count))
    image_count += 1
    plt.close()
    # plt.show()
    # plt.pause(0.1)
    # plt.show()
# plt.ioff()
# plt.show()

history_file = open('history.p', 'wb+')
pickle.dump(history, history_file)