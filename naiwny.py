import itertools

from networkx import path_graph
from visualisation import graf,attraction_list,attraction_names
from itertools import permutations

G = graf(attraction_list,attraction_names)

def naive(graph):
    list_without_start = []
    shortest_path = None
    min_distance = 99999 # jakas duza liczba zeby dzialalo
    
    for attraction in list(graph.nodes()):
        if attraction != "dworzec główny":
            list_without_start.append(attraction)
    print(list_without_start)
            
    for path in itertools.permutations(list_without_start):
       
        path = ["dworzec główny"] +list(path) + ["dworzec główny"]
        print(f"path = {path}")
        
        travel_distance = sum(graph[path[i-1]][path[i]]['weight'] for i in range(1,len(path)))
        print(travel_distance)
        
        if travel_distance < min_distance:
            min_distance = travel_distance
            shortest_path = path
    
    
    print(f"shortest path = {shortest_path}, distance = {min_distance}")
    


naive(G)