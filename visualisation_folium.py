import matplotlib.animation as animation
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib import image as mpimg
from scipy.spatial import distance_matrix
import folium
from folium.plugins import AntPath
from folium.raster_layers import ImageOverlay

from Held_Karp import held_karp
from naiwny import naive
from nearest_neighbor import neighbor
from smallest_edge import smallest_edge

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
    ]
)


def plots(attraction_list, attraction_names):
    # image = mpimg.imread("wroclaw.png")
    # plt.imshow(image)
    # plt.show()
    # # solution = np.arange(attraction_list.shape[0])
    # plt.imshow(image)

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
    plt.gca().invert_yaxis()
    plt.savefig('graf_test.png', transparent=True)
    plt.show()




def graf(attraction_list, attraction_names):
    from scipy.spatial import distance_matrix

    distance_matrix = distance_matrix(attraction_list, attraction_list)
    G = nx.from_numpy_array(distance_matrix)
    mapping = {i: name for i, name in enumerate(attraction_names)}
    G = nx.relabel_nodes(G, mapping)
    return G, distance_matrix


def draw_graph(G):
    pos = nx.spring_layout(G)
    """
    nx.draw_networkx_nodes(G, pos, node_size=700)

    nx.draw_networkx_edges(G, pos)

    nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    pos = nx.spring_layout(G)
    """
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
        if attraction == 'dworzec główny':
            path.append((51.09807213576033,17.03793319537052))
        elif attraction == "hydropolis":
            path.append((51.104241001748285,17.05668290900629))
        elif attraction == "hala stulecia":
            path.append((51.10659103797577,17.077157818694637))
        elif attraction == "katedra":
            path.append((51.114180094231095,17.0473144872636))
        elif attraction == "most tumski":
            path.append((51.1147002202067,17.04229982902))
        elif attraction == "hala targowa":
            path.append((51.11232146521399,17.04033430613034))
        elif attraction == "rynek":
            path.append((51.11031592131893,17.031330666123345))
        elif attraction == "skytower":
            path.append((51.09448052082817,17.019795020806292))
        elif attraction == "opera":
            path.append((51.10558175178294,17.030959447347946))
    return path


def map_visualisation(naive, held_karp, nearest, smallest):

    mapObj = folium.Map(location=[51.11065, 17.035341], zoom_start=13)

    path_naive = path_coordinates(naive)
    path_held_karp = path_coordinates(held_karp)
    path_nearest = path_coordinates(nearest)
    path_smallest = path_coordinates(smallest)

    AntPath(path_naive, delay=400, weight=3, color="red", pulse_color="orange", dash_array=[10,15]).add_to(mapObj)
    AntPath(path_held_karp, delay=400, weight=3, color="blue", pulse_color="green", dash_array=[10, 15]).add_to(mapObj)
    AntPath(path_nearest, delay=400, weight=3, color="purple", pulse_color="blue", dash_array=[10, 15]).add_to(mapObj)
    AntPath(path_smallest, delay=400, weight=3, color="yellow", pulse_color="red", dash_array=[10, 15]).add_to(mapObj)

    ImageOverlay(
        image="graf_test.png",
        bounds=[[51.115, 17.015], [51.091, 17.086]],  # Zaktualizuj granice odpowiednio do lokalizacji
        opacity=1,  # Ustaw przezroczystość obrazu
        interactive=True,
        cross_origin=False
    ).add_to(mapObj)

    mapObj.save("output.html")

if __name__ == "__main__":
    # plots(attraction_list, attraction_names)
    G, distance_matrix = graf(attraction_list, attraction_names)
    # draw_graph(G)
    print("naive")
    naive(G)
    print("Held Karp")
    held_karp(distance_matrix,attraction_names)
    print("nearest neighbor")
    neighbor(G, distance_matrix)
    print("smallest edge")
    smallest_edge(G)
    map_visualisation(['dworzec główny', 'hydropolis', 'hala stulecia', 'katedra', 'most tumski', 'hala targowa', 'rynek', 'opera', 'skytower', 'dworzec główny'],
                      ['dworzec główny', 'hydropolis', 'hala stulecia', 'katedra', 'most tumski', 'hala targowa', 'rynek', 'opera', 'skytower', 'dworzec główny'],
                      ['dworzec główny', 'opera', 'rynek', 'hala targowa', 'most tumski', 'katedra', 'hydropolis', 'hala stulecia', 'skytower', 'dworzec główny'],
                      ['dworzec główny', 'opera', 'rynek', 'hala targowa', 'most tumski', 'katedra', 'hydropolis', 'hala stulecia', 'skytower', 'dworzec główny'])
