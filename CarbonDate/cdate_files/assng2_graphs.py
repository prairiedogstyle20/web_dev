#! /usr/bin/env python3

import matplotlib.pyplot as plt
import os
import json
import time
import traceback
import datetime

def extract_memento_count(search_dir):
    mem_count = []
    links = []
    no_mem_counter = 0
    path, dirs, files = os.walk(search_dir).__next__()
    f_count = len(files)

    for i in range(f_count):
        curr_file = f'{search_dir}/{i}.txt'
        try:
            with open(curr_file) as f:
                mem_count.append(f.readline().rstrip())
                if mem_count[-1] == '0':
                    links.append(None)
                    no_mem_counter += 1
                else:
                    data = json.load(f)
                    links.append(data['original_uri'])
        except Exception as e:
            #traceback.print_exc()
            pass

    return mem_count, links, no_mem_counter

def bin_seperator(data_dict):
    bins = ['0','1','2','3-15','16-50','51-100', '101- 20000']
    totals = [0 for x in bins]

    for each in list(data_dict.keys()):
        if each == '0':
            totals[0] += data_dict.get(each)
        elif each == '1':
            totals[1] += data_dict.get(each)
        elif each == '2':
            totals[2] += data_dict.get(each)
        elif int(each) <= 15:
            totals[3] += data_dict.get(each)
        elif int(each) > 15 and int(each) <= 50:
            totals[4] += data_dict.get(each)
        elif int(each) > 50 and int(each) <= 100:
            totals[5] += data_dict.get(each)
        elif int(each) > 100 and int(each) <= 20000:
            totals[6] += data_dict.get(each)

    return bins, totals

def gen_histogram(mem_count_list):

    data_dict = dict((x,mem_count_list.count(x))for x in set(mem_count_list))
    labels, values = bin_seperator(data_dict)

    name = [i for i in range(len(values))]

    h_graph = plt.bar(name, values)
    n = 0
    for each in h_graph:
        xcord = each.get_x() + (each.get_width() * .5)
        ycord = each.get_y() + each.get_height()
        plt.text(xcord,ycord, str(values[n]))
        n += 1

    plt.xticks(name, labels)
    plt.ylabel('Frequency')
    plt.xlabel('Total Mementos')
    plt.title('Total Mementos vs Frequency')
    plt.savefig('memgator_graph.png')
    plt.show()

def gen_carbon_date_graph(links, mem_count, search_dir):

    path, dirs, files = os.walk(search_dir).__next__()
    f_count = len(files)

    temp_dict = dict(zip(links, mem_count))

    x_values = []
    y_values = []
    today_time_obj = datetime.datetime.today()

    number_creation = 0
    for i in range(f_count):

        curr_file = f'{search_dir}/c{i}.txt'
        try:
            with open(curr_file) as f:
                data = json.load(f)
                if data['estimated-creation-date'] != "":
                    mem_c = temp_dict.get(data['uri'])
                    if mem_c != None and mem_c != 0 and int(mem_c) < 15000:
                        memento_time_obj = datetime.datetime.strptime(data['estimated-creation-date'], "%Y-%m-%dT%H:%M:%S")
                        time_days = today_time_obj - memento_time_obj
                        x_values.append(int(time_days.days))
                        y_values.append(int(mem_c))
                else:
                    number_creation += 1

        except Exception:
            traceback.print_exc()
    #sort_list = zip(x_values, y_values)
    #sorted_list = sorted(sort_list, key=lambda x:x[0])
    #temp_list = list(zip(*sorted_list))
    #x_values = temp_list[0]
    #y_values = temp_list[1]
    graph_2 = plt.scatter(x_values, y_values)
    plt.ylabel('No. of Mementos')
    plt.xlabel('Days')
    plt.title('Days vs Number of Mementos')
    plt.savefig('carbon_date_graph.png')
    plt.show()

    return number_creation

def sortTuple(x):
    return x[1]

def main():
    dir = 'mgator_files'
    c_dir = 'cdate_files'

    count,links, no_mementos = extract_memento_count(dir)

    gen_histogram(count)
    number_creation = gen_carbon_date_graph(links, count, c_dir)
    print("Total URI's: ",len(links))
    print("no mementos: ", no_mementos)
    print('no date estimate: ', number_creation)

main()
