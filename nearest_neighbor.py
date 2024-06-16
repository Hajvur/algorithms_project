def neighbor(graph, distance_matrix, start_point=None):
    end_path = []
    len_path = 0

    if start_point is None:
        for attraction in list(graph.nodes()):
            if attraction == "dworzec główny":
                start_point = attraction
                end_path.append(start_point)
                break
    else:
        end_path.append(start_point)

    while len(end_path) < len(distance_matrix):
        nearest = None
        dist = 9999999  # znowu duża liczba żeby działało

        for start, end, distance in graph.edges(data=True):
            distance = list(distance.values())[0]

            if start == start_point and distance < dist and end not in end_path:
                dist = distance

                nearest = end

            elif end == start_point and distance < dist and start not in end_path:
                dist = distance
                nearest = start

        if nearest is None:
            break

        start_point = nearest
        end_path.append(nearest)
        len_path += dist

    end_path.append("dworzec główny")
    print("_______________Nearest Neighbor Algorithm_______________")
    print(f"path = {end_path}\n")
    len_path += graph[start_point]["dworzec główny"]["weight"]
    print(f"distance = {round(len_path,2)} km")
    return end_path, round(len_path,2)
