import pygame
import random
import numpy as np

points = []
r = 5

def draw_near(x, y):
    points.append((x, y))
    flags.append('red')
    k = random.randint(1, 4)
    d = list(range(-5*r, -2*r)) + list(range(2*r, 5*r))
    for i in range(k):
        x_new = x + random.choice(d)
        y_new = y + random.choice(d)
        points.append((x_new, y_new))
        flags.append('red')

def draw_pygame():
    global flags
    global cache_colors
    clusters = []
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    #окрашиваем
    screen.fill('WHITE')
    play = True
    #чтоб окно быстро не закрывалось и закрывалось на крестик
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    draw_near(event.pos[0], event.pos[1])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    clusters = green_and_yellow()

            screen.fill('WHITE')
            for i in range(len(points)):
    #при нажатии на кнопку мыши, рисуем круг на нашем скрине, красного цвета, координаты, event.pos - на месте нажатия, радиус 5
                pygame.draw.circle(screen, flags[i], ((points[i][0], points[i][1])), r)
            if len(clusters) > 0:
                for cluster in clusters:
                    for i in range(len(cluster)):
                        pygame.draw.circle(screen, cluster[i][2], (cluster[i][0], cluster[i][1]), r)

        pygame.display.update()

def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def color_for_cluster(index):
    if index >= len(cache_colors):
        for i in range(len(cache_colors) - index + 1):
            cache_colors.append(random_color())
    return cache_colors[index]

def random_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

def green_and_yellow():
    # находим зелёные
    for i in range(len(points)):
        neighb = 0
        for j in range(len(points)):
            if dist(points[i], points[j]) <= eps and i != j:
                neighb +=1
        if neighb >= minPts:
            flags[i] = 'green'

    closest_greens = {}
    # находим жёлтые
    for i in range(len(points)):
        closest_green = None
        if flags[i] != 'green':
            for j in range(len(points)):
                if flags[j] == 'green':
                    if dist(points[i], points[j]) <= eps and i != j:
                        flags[i] = 'yellow'
                        closest_green = points[j]
        if closest_green is not None:
            closest_greens.setdefault(closest_green, []).append(points[i])

    # находим красные
    for i in range(len(points)):
        if flags[i] == 0:
            flags[i] = 'red'

    full_points = []
    for i in range(len(points)):
        if flags[i] != 'red' and flags[i] != 'yellow':
            full_points.append([points[i][0], points[i][1], flags[i]])

    clusters = []
    while len(full_points) > 0:
        cluster = [full_points.pop(0)]

        # добавляем точку в кластер
        for point1 in cluster:
            for point2 in full_points:
                if point1 is point2:
                    continue
                if dist(point1, point2) <= eps:
                    if point2 not in cluster:
                        full_points.remove(point2)
                        cluster.append(point2)

        # добавляем жёлтые точки
        yellows_in_cluster = []
        for point_green in cluster:
            [x, y, color] = point_green
            if (x, y) in closest_greens:
                yellows_array = closest_greens[(x, y)]
                for i in range(len(yellows_array)):
                    yellows_in_cluster.append([yellows_array[i][0], yellows_array[i][1], color])
        cluster.extend(yellows_in_cluster)
        clusters.append(cluster)

    for cluster_index, cluster in enumerate(clusters):
        color = color_for_cluster(cluster_index)
        for i in range(len(cluster)):
            cluster[i][2] = color

    return clusters

if __name__ == '__main__':
    points = []
    cache_colors = []
    flags = []
    minPts, eps = 3, 20
    r = 4
    draw_pygame()
