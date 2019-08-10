#! /usr/bin/env python3
import pickle
import json
import requests
import sys
import concurrent.futures
from urllib.parse import urlparse

def json_link_extractor(in_file):

    master_list = []
    links = []

    with open(in_file,'rb') as f:
        for i in range(3):
            temp = pickle.load(f)
            master_list = master_list + temp

    for each in master_list:
        p_json = json.loads(each)
        try:
            urlDic = p_json['entities']['urls'][0]['expanded_url']
            links.append(urlDic)
        except:
            continue

    print(len(str(links)))
    #input()
    return links

def load_url(url):
    res = requests.head(url, headers={'Connection':'close'}, allow_redirects=True,timeout=10)
    return res.url

def link_validator(link_list, o_file):

    valid_links = []
    i = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

        reqObj = {executor.submit(load_url,link):link for link in link_list}
        for future in concurrent.futures.as_completed(reqObj):
            temp_id = reqObj[future][0]

            try:
                unwound_link = future.result()
            except:
                pass
            i += 1
            valid_links.append(unwound_link)
            print(str(i))

    final_links = remove_unwanted_url(valid_links)

    with open(o_file, 'wb') as outf:
        pickle.dump(final_links, outf)
#
# This code is an example given by Professor Nwala
# I found it to be succinct and hard to improve so
#
def canonicalizeURI(uri):

    uri = uri.strip()
    if len(uri) == 0:
        return None

    exceptionDomains = ['www.youtube.com']
    unwantedDomain = ['twitter.com']

    try:
        scheme, netloc, path, params, query, fragment = urlparse(uri)

        netloc = netloc.strip()
        path = path.strip()
        optionalQuery = ''

        if len(path) != 0:
            if path[-1] != '/':
                path = path + '/'

        if netloc.lower() in unwantedDomain:
            return None

        if netloc in exceptionDomains:
            optionalQuery = query.strip()

        return netloc + path + optionalQuery
    except:
        print('Error URI: ', uri)

    return None

def remove_unwanted_url(link_list):
    final_list = []

    for each in link_list:
        temp_link = canonicalizeURI(each)
        if temp_link == None:
            continue
        else:
            final_list.append(each)

    return list(set(final_list))

def main():
    in_file = 'out.txt'
    o_file = 'links.txt'
    temp_links = json_link_extractor(in_file)
    link_validator(temp_links, o_file)


main()
