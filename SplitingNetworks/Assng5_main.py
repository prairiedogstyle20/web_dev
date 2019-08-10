#! /usr/bin/env python3

import graph
import pprint
import operator
import networkx as ntx
import json
import matplotlib.pyplot as plt
import copy

def convert_d3(graph_data, num):

    test = ntx.node_link_data(graph_data)

    if num == 1:
        file = 'karate_club_data_begin.json'
    else:
        file = 'karate_club_data_end.json'

    with open(file, 'w') as f:
        json.dump(test, f)


def data_extractor(data_file):
    node_array_data = [[]for i in range(34)]

    with open(data_file) as f:
        for i in range(34):
            currLine = f.readline().split()
            for x in range(34):
                node_array_data[x].append(currLine[x])

    return node_array_data

def convert_data_for_gaph(matrix_data, graph_object):
    temp_neighbors = []
    for i in range(len(matrix_data)):
        if i == 0:
            name = 'John A'
        elif i == 33:
            name = 'Mr Hi'
        else:
            name = str(i)
        for j in range(34):
            if matrix_data[i][j] == '0':
                continue
            elif matrix_data[i][j] == '1':
                if j == 0:
                    temp_neighbors.append('John A')
                elif j == 33:
                    temp_neighbors.append('Mr Hi')
                else:
                    temp_neighbors.append(str(j))
        graph_object.add_node(name, temp_neighbors)
        temp_neighbors.clear()

def main():
    data_file = 'karate_club_data_matrix.txt'
    matrix_data = data_extractor(data_file)

    karate_graph = graph.Graph()
    convert_data_for_gaph(matrix_data, karate_graph)
    karate_graph.calc_edges()

    temp_graph = ntx.Graph()
    for each in karate_graph.node_collection.keys():
        temp_graph.add_node(each)
    temp_graph.add_edges_from(karate_graph.edges.keys())

    convert_d3(temp_graph, 1)

    color_map = []
    for node in temp_graph:
        if node == "Mr Hi":
            color_map.append('red')
        elif node == "John A":
            color_map.append('green')
        elif int(node) <= 13 and int(node) != 9:
            color_map.append('green')
        elif node == "19" or node == "21" or node == "16" or node == "17":
            color_map.append('green')
        else:
            color_map.append('red')

    ntx.draw(temp_graph,node_color=color_map, with_labels = True)
    plt.savefig('graph_begin.png')
    plt.show()


    while ntx.number_connected_components(temp_graph) != 2:
        remove_edge_data = ntx.edge_betweenness_centrality(temp_graph)
        edge_to_remove = sorted(remove_edge_data.items(),key = lambda x:x[1], reverse = True)[0]
        print(edge_to_remove)

        temp_graph.remove_edge(edge_to_remove[0][0], edge_to_remove[0][1])

    convert_d3(temp_graph, 2)
    ntx.draw(temp_graph,node_color=color_map, with_labels = True)
    plt.savefig('graph_end.png')
    plt.show()

main()
