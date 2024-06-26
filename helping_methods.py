import random
import time

import matplotlib.pyplot as plt
from tabulate import tabulate

from Held_Karp import held_karp
from naiwny import naive
from nearest_neighbor import neighbor
from smallest_edge import smallest_edge
from visualisation_folium import graf


def monte_carlo(attraction_names, coordinates_list, num_iterations):
    subsets_sizes = [3, 5, 7, 10]
    results = {
        size: {
            "naive": [],
            "held_karp": [],
            "nearest_neighbor": [],
            "smallest_edge": [],
        }
        for size in subsets_sizes
    }
    table_data = []

    for size in subsets_sizes:
        for iteration in range(num_iterations):
            subset_names = ["dworzec główny"] + random.sample(
                attraction_names[1:], (size - 1)
            )
            subset_indices = [attraction_names.index(name) for name in subset_names]
            subset_coordinates = [coordinates_list[index] for index in subset_indices]

            G, distance_matrix = graf(subset_coordinates, subset_names)

            start_time = time.perf_counter_ns()
            naive_path, naive_dist = naive(G)
            naive_time = time.perf_counter_ns() - start_time
            results[size]["naive"].append(naive_time)

            start_time = time.perf_counter_ns()
            held_karp_path, held_karp_dist = held_karp(distance_matrix, subset_names)
            held_karp_time = time.perf_counter_ns() - start_time
            results[size]["held_karp"].append(held_karp_time)

            start_time = time.perf_counter_ns()
            nearest_path, nearest_dist = neighbor(G, distance_matrix)
            nearest_time = time.perf_counter_ns() - start_time
            results[size]["nearest_neighbor"].append(nearest_time)

            start_time = time.perf_counter_ns()
            smallest_path, smallest_dist = smallest_edge(G)
            smallest_time = time.perf_counter_ns() - start_time
            results[size]["smallest_edge"].append(smallest_time)

            if iteration == num_iterations - 1:
                paths =[naive_path, held_karp_path, nearest_path, smallest_path]
                path_data = [[attraction_names.index(name) for name in path] for path in paths]
                table_data.extend(
                    [
                        [
                            "naive",
                            size,
                            "->".join(map(str, path_data[0])),
                            naive_time,
                            naive_dist,
                        ],
                        [
                            "held_karp",
                            size,
                            "->".join(map(str, path_data[1])),
                            held_karp_time,
                            held_karp_dist,
                        ],
                        [
                            "nearest_neighbor",
                            size,
                            "->".join(map(str, path_data[2])),
                            nearest_time,
                            nearest_dist,
                        ],
                        [
                            "smallest_edge",
                            size,
                            "->".join(map(str, path_data[3])),
                            smallest_time,
                            smallest_dist,
                        ],
                    ]
                )

    print(
        tabulate(
            table_data,
            headers=["Algorytm", "próba", "Trasa", "Czas(ns)", "Długość trasy"],
            tablefmt="pipe",
        )
    )

    return results, naive_path, held_karp_path, nearest_path, smallest_path


def plot_results(results):
    algorithms = ["naive", "held_karp", "nearest_neighbor", "smallest_edge"]
    subset_sizes = [3, 5, 7, 10]

    fig, axs = plt.subplots(1, 4, figsize=(20, 5))

    for i, algo in enumerate(algorithms):
        avg_times = [
            sum(results[size][algo]) / len(results[size][algo]) for size in subset_sizes
        ]
        min_times = [min(results[size][algo]) for size in subset_sizes]
        max_times = [max(results[size][algo]) for size in subset_sizes]

        axs[i].plot(subset_sizes, avg_times, label="Average Time", marker="o")
        axs[i].plot(subset_sizes, min_times, label="Min Time", marker="o")
        axs[i].plot(subset_sizes, max_times, label="Max Time", marker="o")
        axs[i].set_title(algo.replace("_", " ").title())
        axs[i].set_xlabel("Subset Size")
        axs[i].set_ylabel("Time (ns)")
        axs[i].grid(True)
        axs[i].legend()

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))

    for algo in algorithms:
        if algo != "naive":
            avg_times_all = []
            for size in subset_sizes:
                avg_time = sum(results[size][algo]) / len(results[size][algo])
                avg_times_all.append(avg_time)
            plt.plot(subset_sizes, avg_times_all, label=algo)

    plt.legend()
    plt.title("Średnie czasy wykonania algorytmów (bez algorytmu naiwnego)")
    plt.xlabel("Rozmiar podzbioru")
    plt.ylabel("Średni czas (ns)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
