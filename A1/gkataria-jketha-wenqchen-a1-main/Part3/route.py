#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Gautam, Kataria (gkataria)
#          Jaya Sandeep, Ketha (jketha)
#          Wenqian, Chen (wenqchen)
#
# Based on skeleton code by B551 Course Staff, Fall 2023
#


# !/usr/bin/env python3
import numpy as np
import math
import sys

def loadData():
    # load nodes: cities
    node_f = open("city-gps.txt", "r", encoding="utf8")
    nodes = {}
    for line in node_f.readlines():
        elements = line.strip().split(" ")
        city = elements[0]
        gps0 = float(elements[1])
        gps1 = float(elements[2])
        nodes[city] = [gps0, gps1]
    node_f.close()

    # load lacked nodes
    edge_f = open("road-segments.txt", "r", encoding="utf8")
    for line in edge_f.readlines():
        elements = line.strip().split(" ")
        city0 = elements[0]
        city1 = elements[1]
        if city0 not in nodes:
            nodes[city0] = [None, None]
        if city1 not in nodes:
            nodes[city1] = [None, None]
    edge_f.close()
    node_list = list(nodes.keys())

    # load edge: roads
    edge_f = open("road-segments.txt", "r", encoding="utf8")
    lengths = np.zeros((len(node_list), len(node_list)))
    speed_limits = np.zeros((len(node_list), len(node_list)))
    hwys = None
    # hwys = np.zeros((len(node_list), len(node_list))).tolist()
    for line in edge_f.readlines():
        elements = line.strip().split(" ")
        city0 = elements[0]
        city1 = elements[1]
        length = float(elements[2])
        speed_limit = float(elements[3])
        hwy_name = elements[4]

        city0_i = node_list.index(city0)
        city1_i = node_list.index(city1)
        lengths[city0_i, city1_i] = length
        lengths[city1_i, city0_i] = length
        speed_limits[city0_i, city1_i] = speed_limit
        speed_limits[city1_i, city0_i] = speed_limit
    #     hwys[city0_i][city1_i] = hwy_name
    #     hwys[city1_i][city0_i] = hwy_name
    # hwys = np.array(hwys)
    edge_f.close()

    return node_list, nodes, lengths, speed_limits, hwys


def find_neighbor(node, node_list, lengths):
    neighbors = []
    for i, length in enumerate(lengths[node_list.index(node)]):
        if length > 0:
            neighbors.append(node_list[i])
    return neighbors


def h_function(mode, node0, node1, coordinate, length, speed_limits):
    if mode == "distance":
        # h is time under shortest road
        [node0_x, node0_y] = coordinate[node0]
        [node1_x, node1_y] = coordinate[node1]
        if node0_x is None or node1_x is None:
            dist = 0
        else:
            dist = 54 * math.sqrt(pow((node0_x - node1_x), 2) + pow((node0_y - node1_y), 2))
        return dist
    elif mode == "segments":
        # h is # segments with the highest road length in the shortest distance between two cities
        [node0_x, node0_y] = coordinate[node0]
        [node1_x, node1_y] = coordinate[node1]
        if node0_x is None or node1_x is None:
            dist = 0
        else:
            dist = 54 * math.sqrt(pow((node0_x - node1_x), 2) + pow((node0_y - node1_y), 2))
        return dist // np.max(length)
        # return 1
    elif mode == "time":
        # h is time under shortest road and highest speed
        [node0_x, node0_y] = coordinate[node0]
        [node1_x, node1_y] = coordinate[node1]
        if node0_x is None or node1_x is None:
            dist = 0
        else:
            dist = 54 * math.sqrt(pow((node0_x - node1_x), 2) + pow((node0_y - node1_y), 2))
        return dist/(np.max(speed_limits) + 5)
    elif mode == "delivery":
        # h is # accidents under shortest road and lowest speed limit
        [node0_x, node0_y] = coordinate[node0]
        [node1_x, node1_y] = coordinate[node1]
        if node0_x is None or node1_x is None:
            dist = 0
        else:
            dist = 54 * math.sqrt(pow((node0_x - node1_x), 2) + pow((node0_y - node1_y), 2))
        accidents = 0.000001 * np.min(speed_limits) * dist
        return accidents


def astar_search(initial_node, goal_node, mode, city_list, cities_coordinate, road_len, road_limit):
    closed_set = set()  # set of nodes already evaluated
    nodes = set()  # set of tentative nodes to be evaluated
    nodes.add(initial_node)

    visited = {}  # map of navigated nodes
    g_score = {initial_node: 0}  # distance from start along optimal path
    h_score = {initial_node: h_function(mode, initial_node, goal_node, cities_coordinate, road_len, road_limit)}  # heuristic estimate
    f_score = {initial_node: h_score[initial_node]}  # estimated dist

    while nodes:
        x = None
        for node in nodes:     # pick the shortest distance node
            if x is None:
                x = node
            elif f_score[node] < f_score[x]:
                x = node
        # print(f_score[x])

        nodes.remove(x)
        if x == goal_node:
            return visited

        closed_set.add(x)
        for y in find_neighbor(x, city_list, road_len): # calculate the distance
            if y in closed_set:
                continue
            tentative_g_score = g_score[x] + G_function(mode, x, y, city_list, road_len, road_limit)

            flag = False
            if y not in nodes or tentative_g_score < g_score[y]:
                nodes.add(y)
                flag = True

            if flag:
                visited[y] = x

                g_score[y] = tentative_g_score
                h_score[y] = h_function(mode, y, goal_node, cities_coordinate, road_len, road_limit)
                f_score[y] = g_score[y] + h_score[y]
                # print(g_score[y])
                # print(h_score[y])

    return False

def G_function(mode, node0, node1, node_list, lengths, speed_limits):
    if mode == "distance":
        node0_i = node_list.index(node0)
        node1_i = node_list.index(node1)
        return lengths[node0_i, node1_i]
    elif mode == "segments":
        return 1
    elif mode == "time":
        node0_i = node_list.index(node0)
        node1_i = node_list.index(node1)
        return lengths[node0_i, node1_i] / (speed_limits[node0_i, node1_i] + 5)
    elif mode == "delivery":
        node0_i = node_list.index(node0)
        node1_i = node_list.index(node1)
        segment_len = lengths[node0_i, node1_i]
        segment_limit = speed_limits[node0_i, node1_i]
        
        if segment_limit >= 50:
            # Calculate the probability of a package falling out using tanh
            p = math.tanh(segment_len / 1000)
            # Calculate the expected time considering the package falling out
            return segment_len + p * 2 * (segment_len / (segment_limit + 5))
        else:
            # If speed limit is < 50 mph, no chance of package falling out
            return segment_len


def get_route(start, end, cost):

    node_list, nodes, lengths, speed_limits, hwys = loadData()
    
    if start not in nodes or end not in nodes:
        raise Exception("Error: Start or end city not found in the data.")
    
    visited = astar_search(start, end, cost, node_list, nodes, lengths, speed_limits)

    if not visited:
        raise Exception("Error: No route found between {} and {} using {} cost.".format(start, end, cost))

    all_distance = 0
    all_segments = []
    all_hours = 0
    path = [end]
    now = end

    while True:
        former = visited[now]

        former_i = node_list.index(former)
        now_i = node_list.index(now)
        # calculate all distance
        segment_len = lengths[former_i, now_i]
        all_distance += segment_len
        # calculate all hours
        segment_limit = speed_limits[former_i, now_i]
        segment_hours = segment_len / (segment_limit + 5)
        all_hours += segment_hours
        # calculate all segments
        segment = [former_i, now_i]
        if segment not in all_segments:
            all_segments.append(segment)
        # list all paths
        path = [former] + path

        now = former
        if now == start:
            break

    route_taken = []
    for i in range(len(path) - 1):
        segment_info = "Segment from {} to {} ({} miles)".format(path[i], path[i + 1], lengths[node_list.index(path[i]), node_list.index(path[i + 1])])
        route_taken.append((path[i+1], segment_info))

    return {
        "total-segments": len(all_segments),
        "total-miles": all_distance,
        "total-hours": all_hours,
        "total-delivery-hours": all_hours,
        "route-taken": route_taken
    }

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise Exception("Error: expected 3 arguments")

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise Exception("Error: invalid cost function")

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


