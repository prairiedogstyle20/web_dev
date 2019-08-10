# /usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup as BS

'''
  This program will take a URL as a command line argument
  retrieve the links from the URL, then for each link
  a head request will be made. If status code is 200 and
  the content-type is application/pdf then the link name
  and the content-length will be printed to standard out
'''

def main():

    # invoke request library to make a get call to the URL passed as
    # the command line argument
    try:
        response = requests.get(sys.argv[1])
    except:
        print('There was an issue with the URL please try again')

    # invoke the beautiful soup library html parser to split the response body
    # form the returned request object
    soup_OBJ = BS(response.text, 'html.parser')

    # for each link in the object returned from find_all method
    # the link is checked to see if the link is absolute, site root relative,
    # or relative and adjusts the links before making the head request
    for link in soup_OBJ.find_all('a'):
        curr_Link = link.get('href')


        # if no links are found return
        if curr_Link == None:
            break

        # skip all comments
        if curr_Link[0] == '#':
            continue

        # check for site relative links
        elif curr_Link[0] == '/':
            link = sys.argv[1] + curr_Link

        # check for relative links
        elif curr_Link[:4] != 'http':
            link = sys.argv[1]+'/'+curr_Link

        # used for absolute links
        else:
            link = curr_Link

        # makes head request based on the possibly modified link object
        try:
            res = requests.head(link,allow_redirects=True)
        except:
            continue

        # checks for conditions of successful transaction and the type of data
        # then outputs to stdout
        if res.status_code == 200 and res.headers['content-type'] == 'application/pdf':
            print('link: ' + link)
            print('content-length: ' + res.headers['content-length'] + ' bytes')

main()
