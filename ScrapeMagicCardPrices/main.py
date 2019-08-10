#! /usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse
import string

def main():

    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    browser.get("http://www.magicspoiler.com/war-of-the-spark-card-list/")

    data = browser.execute_script("return document.body.innerHTML")

    soup_OBJ = BS(data, 'html.parser')

    card_names = []
    converted_names = []
    for link in soup_OBJ.find_all('a'):
        if link.text != None and '.' in link.text:
            temp = link.text.split('.')
            try:
                if int(temp[0]) <= 275:
                    card_names.append(temp[1])
            except:
                pass

    for each in card_names:
        each = "".join([c for c in each if c in string.ascii_letters or c in string.whitespace or c =="-"])

        each = each.replace(" ", "-")
        if each[0] == '-':
            each = each[1:]
        if each[len(each)-1] == '-':
            each = each[:len(each)-1]
        each = each.lower()
        converted_names.append(each)

    results = []
    num_counter = 0
    with open('foil_prices.txt', 'w') as f:
        for each in converted_names:
            url = f"https://shop.tcgplayer.com/magic/war-of-the-spark/{each}"
            print(url)

            browser.get(url)

            data = browser.execute_script("return document.body.innerHTML")

            soup_OBJ = BS(data, 'html.parser')
            foil_div = soup_OBJ.find_all("td",{"class":"price-point__data"})
            f.write(card_names[num_counter] + " ")
            f.write(str(foil_div[1]) + "\n")
            num_counter += 1

main()
