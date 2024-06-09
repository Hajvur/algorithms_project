import itertools
from itertools import permutations

from networkx import path_graph


def naive(graph):
    list_without_start = []
    shortest_path = None
    min_distance = 99999  # jakas duza liczba zeby dzialalo

    for attraction in list(graph.nodes()):
        if attraction != "dworzec główny":
            list_without_start.append(attraction)

    for path in itertools.permutations(list_without_start):
        path = ["dworzec główny"] + list(path) + ["dworzec główny"]

        travel_distance = sum(
            graph[path[i - 1]][path[i]]["weight"] for i in range(1, len(path))
        )

        if travel_distance < min_distance:
            min_distance = travel_distance
            shortest_path = path

    print(f"shortest path = {shortest_path}, distance = {min_distance}")
