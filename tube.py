#!/usr/bin/python3

import csv
import networkx as nx
import matplotlib.pyplot as plt
import lxml.etree as etree
import string


class TubeMap:

    def __init__(self):
        self.import_tube_map_svg()
        self.import_travel_times()
        self.import_tube_station_codes()

    def hide_all_stations(self):
        for station_code in self.station_codes.keys():
            station_svg = self.get_svg_station(station_code)
            if station_svg is not None:
                self.hide_element(station_svg)
            else:
                print(station_code)

    def as_graph(self):
        return self.graph

    def get_station_code(self, station_name):
        return self.station_names[string.capwords(station_name)]

    def get_station_name(self, station_code):
        return self.station_codes[station_code]

    def standardise_station(self, s):
        return s if len(s) == 3 and s.isupper() else self.get_station_code(s)

    def hide_stations(self, stations):
        for station in stations:
            self.hide_station(station)

    def show_stations(self, stations):
        for station in stations:
            self.show_station(station)

    def show_station(self, station):
        self.show_element(self.get_svg_station(station))

    def hide_station(self, station):
        self.show_element(self.get_svg_station(station))

    def set_station_opacity(self, station, opacity):
        self.set_element_opacity(self.get_svg_station(station), opacity)

    def hide_element(self, element):
        element.attrib['visibility'] = 'hidden'

    def show_element(self, element):
        element.attrib['visibility'] = 'visible'

    def set_element_opacity(self, element, opacity):
        element.attrib['opacity'] = str(opacity)

    def get_svg_station(self, station):
        station_code = self.standardise_station(station)
        matches = self.svg.xpath(f"//*[name()='svg']//*[@id='{station_code}']")
        if len(matches) != 1:
            raise LookupError(f"Bad station ID {station_code}")
        else:
            return matches[0]

    def output_svg(self, filename):
        etree.ElementTree(self.svg).write(filename)

    def import_tube_map_svg(self):
        self.svg = etree.parse("assets/tube-map-clean-inkscape.svg").getroot()

    def import_tube_station_codes(self):
        self.station_codes = {}
        self.station_names = {}
        with open('assets/tube-station-codes.csv') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in csv_reader:
                station_name, station_code = row
                self.station_codes[station_code] = station_name
                # two-way mapping, bijective
                self.station_names[station_name] = station_code

    def import_travel_times(self):
        self.graph = nx.DiGraph()

        with open('assets/inter-station-train-times.csv') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in csv_reader:
                line, _, station_a, station_b, distance, _, _, time = [
                    el.strip() for el in row]
                self.graph.add_node(station_a)
                self.graph.add_node(station_b)
                self.graph.add_edge(station_a, station_b, weight=float(
                    time), distance=float(distance), line=line)

    def compute_shortest_path(self, station_a, station_b):
        return list(nx.all_shortest_paths(self.graph, station_a, station_b, weight='weigt')), nx.shortest_path_length(self.graph, station_a, station_b, weight='weight')

    def print_to_pdf(self):
        nx.draw(self.graph, node_color='black', edge_color='b', with_labels=True,
                font_size=2, arrows=False, **{"node_size": 1, "alpha": 0.8})
        plt.savefig('map.pdf')
