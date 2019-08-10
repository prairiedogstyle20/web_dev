#! /usr/bin/env python3
import requests
import pickle
import os

def memgator_colect(base_uri, links):
    i = 0
    for each in links:
        test_uri = base_uri + each
        try:
            res = requests.get(test_uri,allow_redirects=True, timeout=10)
            print(str(res.headers['x-Memento-Count']))
            curr_file = f'touch {i}.txt'
            os.system(curr_file)

            with open(f'{i}.txt', 'w') as f:
                f.write( res.headers['x-Memento-Count'] + '\n')
                f.write(res.text)
        except:
            pass
        i += 1

def main():

    base_uri_memgator = 'http://localhost:1208/timemap/json/'

    link_file = 'links.txt'
    with open(link_file, 'rb') as f:
        links = pickle.load(f)

    memgator_colect(base_uri_memgator, links)

main()
