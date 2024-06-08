import matplotlib.animation as animation
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib import image as mpimg
from scipy.spatial import distance_matrix

from naiwny import naive
from Held_Karp import held_karp
from nearest_neighbor import neighbor

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
            color="white",
            size="8",
        )

    plt.show()


def graf(attraction_list, attraction_names):
    from scipy.spatial import distance_matrix

    distance_matrix = distance_matrix(attraction_list, attraction_list)
    print(distance_matrix)
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


if __name__ == "__main__":
    plots(attraction_list, attraction_names)
    G, distance_matrix = graf(attraction_list, attraction_names)
    draw_graph(G)
    # naive(G)
    # held_karp(attraction_list)
    # neighbor(G,distance_matrix)
