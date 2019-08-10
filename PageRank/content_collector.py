#! /usr/bin/env python3
import requests
import sys
import os
import pickle
import hashlib
import concurrent.futures
from boilerpipe.extract import Extractor

def unpickle_list(file):
    with open(file, 'rb') as f:
        link_list = pickle.load(f)
    return link_list

def gen_hash(links):
    hash_list = []
    for each in links:
        hash_list.append(hashlib.md5(each.encode('utf-8')))
    return hash_list

def get_html(url):
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
    return res.text

def collect_html_data(links):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

        future_to_data = {executor.submit(get_html,url): url for url in links}
        for future in concurrent.futures.as_completed(future_to_data):
            try:
                url = future_to_data[future]
                hash_name = hashlib.md5(url.encode('utf-8'))
                html_name = 'response_html/' + hash_name.hexdigest() + '_html'
                extract_name = 'response_boiler/' + hash_name.hexdigest()+ '_boiler'
                #os.system(f'touch response_files/{fname}')
                with open(html_name, 'w') as f:
                    f.write(future.result())

                extractor = Extractor(extractor='ArticleExtractor', html = future.result())
                extract_txt = extractor.getText()

                with open(extract_name, 'w') as ef:
                    ef.write(extract_txt)
            except Exception as e:
                print(sys.exc_info())

def main():
    link_file = 'links.txt'
    links = unpickle_list(link_file)
    hashes = gen_hash(links)
    print(hashes[0].name)
    collect_html_data(links)

    return

main()
