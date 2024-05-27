import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import image as mpimg

image = mpimg.imread("wroclaw.png")
plt.imshow(image)
plt.show()


attraction_names = [
    "hydropolis",
    "hala stulecia",
    "katedra",
    "most tumski",
    "hala targowa",
    "rynek",
    "skytower",
    "opera",
    "dworzec główny",
]
#          wspolrzedne  x    y   jako x,y pikseli obrazu
attraction_list = np.array(
    [
        [599.2, 339.2],  # hydropolis
        [782.4, 274.0],  # hala stulecia
        [421.3, 133.7],  # katedra
        [372.2, 124.5],  # most tumski
        [348.4, 161.3],  # hala targowa
        [244.1, 216.5],  # rynek
        [109.1, 502.5],  # skytower
        [253.3, 303.9],  # opera
        [309.3, 417.4],  # dworzec głowy
    ]
)


solution = np.arange(attraction_list.shape[0])
attraction_location = np.concatenate(
    (
        np.array([attraction_list[solution[i]] for i in range(len(solution))]),
        np.array([attraction_list[0]]),
    )
)


plt.imshow(image)


plt.scatter(attraction_list[:, 0], attraction_list[:, 1])

for i in range(len(attraction_list)):
    for j in range(i + 1, len(attraction_list)):
        plt.plot(
            [attraction_list[i, 0], attraction_list[j, 0]],
            [attraction_list[i, 1], attraction_list[j, 1]],
            "r-",
            lw = 0.5
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