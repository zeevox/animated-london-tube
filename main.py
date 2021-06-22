#!/usr/bin/python3

import string
import tube
from pprint import pprint
from collections import defaultdict
import os
import glob


def clear_dir(dirname):
    files = glob.glob(dirname + "/*")
    for f in files:
        os.remove(f)


global count
count = 0

def draw_frame():
    global count
    count += 1
    tube_map.output_svg(f"out/frames/{count:05}.svg")

def dijkstra(graph, source, target):
    if source not in graph.nodes :
        raise ValueError(f"{source} is not a station")
    elif target not in graph.nodes:
        raise ValueError(f"{target} is not a station")

    clear_dir("out/frames")

    tube_map.hide_all_stations()

    vertices = set(graph.nodes)
    dist = defaultdict(lambda:float('inf'))
    prev = defaultdict(str)

    dist[source] = 0
    while vertices:
        u = min(vertices, key=lambda x: dist[x])
        vertices.remove(u)

        tube_map.show_station(u)
        draw_frame()
        
        if u == target:
            path = []

            for station in (set(graph.nodes) - vertices):
                tube_map.set_station_opacity(station, 0.25)
            tube_map.set_station_opacity(target, 1.0)
            draw_frame()

            while u in prev:
                path.append(u)
                u = prev[u]

                tube_map.set_station_opacity(u, 1.0)
                draw_frame()
            return dist[target], path[::-1]
        
        for v in graph.adj[u]:
            if v not in vertices:
                continue
            alt = dist[u] + graph.edges[u, v]['weight']
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    return None, None


def asciify(s):
    return s.translate(string.punctuation)


def draw_shortest_path(station_a, station_b):
    route, time = tube_map.compute_shortest_path(
        station_a.upper(), station_b.upper())
    pprint(route)
    print(time)

    for station_code in (tube_map.station_names[string.capwords(name)] for name in route[0]):
        print(station_code)
        tube_map.show_element(tube_map.get_svg_station(station_code))

    tube_map.output_svg(f"out/{asciify(station_a)}-{asciify(station_b)}.svg")


def find_longest_shortest_path():
    lengths = dict(nx.all_pairs_dijkstra(tube_map.graph, weight='weight'))
    longest = [None, None, -1]
    for source in lengths.keys():
        furthest = list(lengths[source][0].items())[-1]
        if furthest[1] > longest[2]:
            longest = [source, furthest[0], furthest[1]]
    pprint(longest)


if __name__ == "__main__":
    tube_map = tube.TubeMap()
    dist, path = dijkstra(tube_map.as_graph(), "HEATHROW TERMINAL 4", "MILL HILL EAST")
    pprint(path)
    tube_map.output_svg("out/test.svg")

    #draw_shortest_path("Morden", "Heathrow Terminal 5")
