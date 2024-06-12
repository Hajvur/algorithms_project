import folium
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from folium.plugins import AntPath
from geopy.distance import geodesic
from matplotlib import image as mpimg

attraction_names = [
    "dworzec główny",
    "hydropolis",
    "hala stulecia",
    "katedra",
    "most tumski",
    "hala targowa",
    "rynek",
    "skytower",
    "opera",
    "zoo",
    "panorma racławicka",
    "muzeum narodowe",
    "centrum technologii audiowizualnych",
    "aquapark",
    "park szczytnicki",
    "uniwersytet wrocławski",
    "politechnika wrocławska",
    "polinka",
    "muzeum poczty",
    "plac grunwaldzki",
]
#          wspolrzedne  x    y   jako x,y pikseli obrazu
attraction_list = np.array(
    [
        [309.3, 417.4],  # dworzec głowy
        [599.2, 339.2],  # hydropolis
        [782.4, 274.0],  # hala stulecia
        [421.3, 133.7],  # katedra
        [372.2, 124.5],  # most tumski
        [348.4, 161.3],  # hala targowa
        [244.1, 216.5],  # rynek
        [109.1, 502.5],  # skytower
        [253.3, 303.9],  # opera
        [757.1, 312.4],  # zoo
        [398.7, 207.8],  # panorama raclawicka
        [434.3, 197.6],  # muzeum narodowe
        [744.5, 247.7],  # centrum technologii audiowizualnych
        [249.3, 563.7],  # aquapark
        [827.1, 137.3],  # park szczytnicki
        [284.5, 134.1],  # uniwersytet wrocławski
        [583.0, 228.4],  # politechnika wrocławska
        [508.2, 276.0],  # polinka
        [390.0, 245.5],  # muzeum poczty
        [582.9, 180.8],  # plac grunwaldzki
    ]
)

coordinates_list = np.array(
    [
        [51.09807213576033, 17.03793319537052],  # dworzec główny
        [51.104241001748285, 17.05668290900629],  # hydropolis
        [51.10659103797577, 17.077157818694637],  # hala stulecia
        [51.114180094231095, 17.0473144872636],  # katedra
        [51.1147002202067, 17.04229982902],  # most tumski
        [51.11232146521399, 17.04033430613034],  # hala targowa
        [51.11031592131893, 17.031330666123345],  # rynek
        [51.09448052082817, 17.019795020806292],  # skytower
        [51.10558175178294, 17.030959447347946],  # opera
        [51.10546047455658, 17.076281183233014],  # zoo
        [51.10981301532243, 17.044317107189414],  # panorama racławicka
        [51.11073072469882, 17.04767540584498],  # muzeum narodowe
        [51.10824249215664, 17.07451123731235],  # centrum technologii audiowizualnych
        [51.09008941443009, 17.03251566063438],  # aquapark
        [51.11370454024076, 17.08233940882745],  # park szczytnicki
        [51.113955578104644, 17.03466319639916],  # uniwersytet wrocławski
        [51.10876516242112, 17.060111912653156],  # politechnika wrocławska
        [51.10600826276814, 17.05342293740822],  # polinka
        [51.108275208826214, 17.044330299855616],  # muzeum poczty
        [51.111513675256035, 17.06018831777431],  # plac grunwaldzki
    ]
)


def calculate_distance_matrix(coordinates):
    num_points = len(coordinates)
    distance_matrix = np.zeros((num_points, num_points))

    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                distance_matrix[i, j] = geodesic(
                    coordinates[i], coordinates[j]
                ).kilometers

    return distance_matrix


def plots(attraction_list, attraction_names):
    image = mpimg.imread("wroclaw.png")
    plt.imshow(image)
    plt.show()
    # solution = np.arange(attraction_list.shape[0])
    plt.imshow(image)

    plt.scatter(attraction_list[:, 0], attraction_list[:, 1])

    for i in range(len(attraction_list)):
        for j in range(i, len(attraction_list)):
            plt.plot(
                [attraction_list[i, 0], attraction_list[j, 0]],
                [attraction_list[i, 1], attraction_list[j, 1]],
                "r-",
                lw=0.5,
            )

    for i in range(len(attraction_list)):
        plt.text(
            attraction_list[i, 0],
            attraction_list[i, 1],
            attraction_names[i],
            color="black",
            size="8",
        )
    # plt.gca().invert_yaxis()
    plt.savefig("graf_test.png", transparent=True)
    plt.show()


def graf(coordinates, attraction_names):
    from scipy.spatial import distance_matrix

    distance_matrix = calculate_distance_matrix(coordinates)
    # print(distance_matrix)
    G = nx.from_numpy_array(distance_matrix)
    mapping = {i: name for i, name in enumerate(attraction_names)}
    G = nx.relabel_nodes(G, mapping)
    return G, distance_matrix


def draw_graph(G):
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        edge_color="black",
        node_size=500,
        font_size=10,
    )
    plt.show()


def path_coordinates(attractions):
    path = []
    for attraction in attractions:
        if attraction in attraction_names:
            idx = attraction_names.index(attraction)
            path.append(tuple(coordinates_list[idx]))
        else:
            print(f"Error: {attraction} not found in attraction_names")
    return path


def map_visualisation(naive, held_karp, nearest, smallest):
    mapObj = folium.Map(location=[51.11065, 17.035341], zoom_start=13)

    path_naive = path_coordinates(naive)
    path_held_karp = path_coordinates(held_karp)
    path_nearest = path_coordinates(nearest)
    path_smallest = path_coordinates(smallest)

    AntPath(
        path_naive,
        delay=400,
        weight=3,
        color="red",
        pulse_color="orange",
        dash_array=[10, 15],
    ).add_to(mapObj)
    AntPath(
        path_held_karp,
        delay=400,
        weight=3,
        color="blue",
        pulse_color="green",
        dash_array=[10, 15],
    ).add_to(mapObj)
    AntPath(
        path_nearest,
        delay=400,
        weight=3,
        color="purple",
        pulse_color="blue",
        dash_array=[10, 15],
    ).add_to(mapObj)
    AntPath(
        path_smallest,
        delay=400,
        weight=3,
        color="yellow",
        pulse_color="red",
        dash_array=[10, 15],
    ).add_to(mapObj)
    """
    ImageOverlay(
        image="graf_test.png",
        bounds=[[51.115, 17.015], [51.091, 17.086]],  # Zaktualizuj granice odpowiednio do lokalizacji
        opacity=1,  # Ustaw przezroczystość obrazu
        interactive=True,
        cross_origin=False
    ).add_to(mapObj)
    """
    mapObj.save("output.html")


if __name__ == "__main__":
    plots(attraction_list, attraction_names)
    from helping_methods import monte_carlo

    (
        results,
        path_naive,
        path_held_karp,
        path_neighbour,
        path_edge,
    ) = monte_carlo(attraction_names, coordinates_list, 10)

    G, distance_matrix = graf(coordinates_list, attraction_names)
    draw_graph(G)
    print(results)
    from helping_methods import plot_results

    plot_results(results)
    # rint("naive")
    # path_naive, dist_naive = naive(G)
    # print("Held Karp")
    # path_held_karp, path_held_karp = held_karp(distance_matrix,attraction_names)
    # print("nearest neighbor")
    # path_neighbour, dist_neighbor = neighbor(G, distance_matrix)
    # print("smallest edge")
    # path_edge, dist_edge = smallest_edge(G)
    map_visualisation(
        path_naive,
        path_held_karp,
        path_neighbour,
        path_edge,
    )
