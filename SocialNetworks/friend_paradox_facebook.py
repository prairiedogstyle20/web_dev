#! /usr/bin/env python3

import csv
import matplotlib.pyplot as plt
import numpy
from operator import itemgetter

def main():
    csv_file = 'acnwala-friendscount.csv'
    data_list = parse_csv(csv_file)

    temp_data_list = [x[1] for x in data_list]
    temp_names_list = [x[0] for x in data_list]

    curr_mean,curr_std,curr_median = calc_stats(temp_data_list)

    gen_graph(temp_data_list, temp_names_list, curr_mean, curr_median, curr_std)

def parse_csv(csv_file):
    data_list = []
    with open(csv_file) as f:
        doc_parsed = csv.reader(f, delimiter=',')
        for row in doc_parsed:
            try:
                data_list.append((row[0],int(row[1])))
            except ValueError:
                pass
        return sorted(data_list, key=itemgetter(1))

def calc_stats(data_list):
    data_mean = round(numpy.mean(data_list), 3)
    data_std = round(numpy.std(data_list),3)
    data_median = round(numpy.median(data_list),3)
    print('curr_mean: ', data_mean)
    print('curr_std: ', data_std)
    print('curr_median: ', data_median)
    # returns mean, standard deviation and median in that order
    return data_mean, data_std, data_median

def gen_graph(curr_data_list, names_list, mean, median, std):

    temp_x_values = [x for x in range(len(curr_data_list))]

    ax = plt.plot(temp_x_values, curr_data_list)

    place_nwala = False
    place_mean = False
    place_median = False
    place_std = False

    for i in range(len(curr_data_list)):

        if curr_data_list[i] >= 100 and place_nwala == False:
            plt.plot(i, 100, marker='x',markersize=6, color='red')
            plt.annotate(f'Alexander Nwala: 100',(i,100))
            place_nwala = True
        elif curr_data_list[i] >= mean and place_mean == False:
            plt.plot(i, mean, marker='x',markersize=6, color='red')
            plt.annotate(f'Mean: {mean}',(i,mean+50))
            place_mean = True
        elif curr_data_list[i] >= median and place_median == False:
            plt.plot(i, median, marker='x',markersize=6, color='red')
            plt.annotate(f'Median: {median}',(i,median-150))
            place_median = True
        elif curr_data_list[i] >= std and place_std == False:
            plt.plot(i, std, marker='x',markersize=6, color='red')
            plt.annotate(f'Std: {std}',(i,std-150))
            place_std = True

    plt.title('Chart 1: Friend vs FriendCount(Facebook)')
    plt.xlabel('Friends')
    plt.ylabel('No. of Friends')
    plt.savefig('friend_paradox_facebook.png')

main()
