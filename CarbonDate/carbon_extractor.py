#! /usr/bin/env python3
import requests
import pickle
import os

def main():

    base_uri_carbon_date = 'http://localhost:8888/cd/'

    link_file = 'links.txt'
    with open(link_file, 'rb') as f:
        links = pickle.load(f)

    for i in range(len(links)):
        links[i] = base_uri_carbon_date + links[i]

    i = 0
    for each in links:
        try:
            res = requests.get(each, allow_redirects=True, timeout=20)
            os.system(f'touch cdate_files/c{i}.txt')

            with open(f'cdate_files/c{i}.txt','w') as f:
                f.write(res.text)
            i += 1
        except Exception as e:
            print(e)


main()
