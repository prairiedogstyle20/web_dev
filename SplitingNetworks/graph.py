#! /usr/bin/env python3
import operator

class Node:

    def __init__(self, node_key):
        self.name = node_key
        self. neighbors = {}

    def set_name(self,new_name):
        self.name = new_name

    def add_one_neighbor(self,neighbor_name):
        if self.check_neightbor(neighbor_name) == True:
            return
        else:
            self.neighbors[neighbor_name] = len(self.neighbors) + 1

    def add_neighbors(self,neighbor_list):
        for i in range(len(neighbor_list)):
            self.neighbors[neighbor_list[i]] = i

    def check_neightbor(self,possible_neighbor):
        if self.neighbors.get(possible_neighbor) != None:
            return True
        else:
            return False

    def get_neighbors(self):
        return self.neighbors.keys()

class Graph:

    def __init__(self):
        self.node_collection = {}
        self.edges = {}
        self.vertices = []

    def add_node(self, name, neighbor_list):
        if self.node_collection.get(name) == None:
            temp_node = Node(name)
            self.node_collection[name] = temp_node
            temp_node.add_neighbors(neighbor_list)


    def get_vertices(self):
        return self.node_collection.keys()

    def calc_edges(self):
        for k in self.node_collection:
            for each in self.node_collection[k].get_neighbors():
                if self.edges.get((k,each)) != None or self.edges.get((each,k)) != None:
                    continue
                else:
                    self.edges[(k,each)] = 0

    def go_deeper(self, curr_node, visited_list, curr_queue, path_counter, curr_depth, total_short_paths):

        item_added = False

        visited_list.append(curr_queue.pop(0))

        for every in self.node_collection[curr_node].get_neighbors():
            if every not in visited_list and every not in curr_queue and self.edges.get((curr_node, every)) != None:
                self.edges[(curr_node,every)] += curr_depth
                path_counter[(curr_node,every)] += 1
                total_short_paths += 1
                curr_queue.append(every)
                item_added = True

            elif every not in visited_list and every not in curr_queue and self.edges.get((every, curr_node)) != None:
                self.edges[(every,curr_node)] += curr_depth
                path_counter[(every, curr_node)] += 1
                total_short_paths += 1
                curr_queue.append(every)
                item_added = True
            else:
                continue

        if item_added == True:
            return self.go_deeper(curr_queue[0], visited_list, curr_queue, path_counter, curr_depth + 1, total_short_paths)
            curr_queue.pop(0)
        else:
            return total_short_paths




    def BFS(self):

        queue = []
        sum_of_between = self.edges.fromkeys(self.edges, 0)

        for each in self.node_collection:
            #print('value of each: ', each)
            path_counter = self.edges.fromkeys(self.edges, 0)
            self.edges = self.edges.fromkeys(self.edges, 0)
            depth = 1
            curr_node = each
            total_short_paths = 0
            queue.append(each)
            visited_nodes = [each]
            total_short_paths = self.go_deeper(curr_node, visited_nodes, queue, path_counter, depth, total_short_paths)
            for p in sum_of_between:
                sum_of_between[p] += path_counter[p]/total_short_paths


            queue.clear()
        print(sorted(sum_of_between.items(), key = operator.itemgetter(1), reverse = True)[0])
        #for each in self.edges:
        #    self.edges[each] /= path_counter[each]
"""
            list_visited = []
            while queue:
                depth += 1

                next_node = queue.pop(0)
                list_visited.append(next_node)
                #print(next_node)
                #input()
                print(depth)
                for every in self.node_collection[next_node].get_neighbors():
                    #print('dictionary value: ',self.edges[(each,every)])

                    if every in list_visited or self.edges.get((each,every)) == None:
                        pass
                    else:
                        #depth += 1
                        self.edges[(each,every)] += depth
                        queue.append(every)
                        list_visited.append(every)

                    if every in list_visited or self.edges.get((every,each)) == None:
                        pass
                    else:
                        #depth += 1
                        self.edges[(each,every)] += depth
                        queue.append(every)
                        list_visited.append(every)
"""
