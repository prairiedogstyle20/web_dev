#! /usr/bin/env python3

import requests
import feedparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse
import urllib
import re
import Clusters
def main():
    #blogs = get_blogs()
    blognames,words,data = Clusters.readfile('blog_data.txt')
    clust = Clusters.hcluster(data)
    for i in range(len(blognames)):
        blognames[i].encode('ascii','ignore')
    Clusters.drawdendrogram(clust, blognames, jpeg='blogcluster.jpg')
    input()
    blogs = []
    with open("blog_urls.txt",'r') as f:
        line = f.readline().rstrip()
        while(line != ''):
            blogs.append(line)
            line = f.readline().rstrip()

    find_popular_words(blogs)

def find_popular_words(blogs):
    accumulated_term_scores = {}
    terms = []
    dict_all_items = {}

    for each in blogs:
        row_name, word_count = get_word_counts(each)
        dict_all_items[row_name] = word_count
        for every in word_count.keys():
            if accumulated_term_scores.get(every) == None:
                accumulated_term_scores[every] = word_count[every]
            else:
                accumulated_term_scores[every] += word_count[every]
    accum_scores = sorted(accumulated_term_scores.items(), key= lambda kv:(kv[1], kv[0]))
    for num in range(1000):
        terms.append(accum_scores[num][0])

    with open("blog_data.txt", 'w') as outf:
        outf.write('Blog' + "\t")
        for y in terms:
            outf.write(y + "\t")
        outf.write("\n")
        for e in dict_all_items.keys():
            new_list = []
            temp_dict = dict_all_items.get(e)
            for all in terms:
                if temp_dict.get(all) == None:
                    new_list.append('0')
                else:
                    new_list.append(str(temp_dict.get(all)))
            outf.write(e +"\t")
            for d in new_list:
                outf.write(d + "\t")
            outf.write("\n")


def get_word_counts(url):
    d = feedparser.parse(url)
    wc={}

    for each in d.entries:
        words = getwords(each.title)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title,wc

def getwords(html):
    # Remove all the HTML tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word != '']

def get_blogs():
    blogger_api_key = 'AIzaSyCIp4k2yRqpir-7w5FIN9GyNNdRHyCwTV0'
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

    blog_links = ["http://f-measure.blogspot.com/atom.xml","http://ws-dl.blogspot.com/atom.xml"]

    query_terms = ["python", "data science", "Cars", "Java" , "Dreams", "Video Games", "Game of Thrones", "cats", "NBA", "baseball", "programming", "Fans", "Math"]
    query_id = 0
    while len(blog_links) != 100:
        selected_term = query_terms[query_id]
        query_id += 1
        url = f'https://www.searchblogspot.com/search?q={selected_term}'
        browser.get(url)
        for each in range(2,11):
            value = str(each)
            data = browser.execute_script("return document.body.innerHTML")

            soup_OBJ = BS(data, 'html.parser')

            for link in soup_OBJ.find_all('a'):
                if link.get('href') != None and "blogspot" in link.get('href'):
                    curr_Link = parse_urls(link.get('href'))
                    if curr_Link not in blog_links and len(blog_links) != 100:
                        blog_links.append(curr_Link)
                        print("Total blogs: ",len(blog_links))

            next_button = browser.find_element_by_xpath("//div[@class='gsc-cursor-page'and contains(text(),value)]")

            act = ActionChains(browser)
            act.move_to_element(next_button).click(next_button).perform()

    with open("blog_urls.txt",'w') as f:
        for each in blog_links:
            f.write(each + '\n')

    return blog_links

def parse_urls(url):
    split_url = urlparse(url)
    return split_url.scheme +'://' +split_url.netloc + '/atom.xml'

main()
