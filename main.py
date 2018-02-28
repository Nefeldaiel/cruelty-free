#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import requests
import urllib2
import re
from lxml import html

empty_string = "-"

def get_text_from_divs(divs):
    if len(divs) > 0:
        return divs[0].text_content()
    return empty_string

def get_attr_from_divs(divs, attr_name):
    if len(divs) > 0:
        return divs[0].get(attr_name)
    return empty_string

#
# Different implementation between using requests and urllib2(python 2.7 pre-installed)
#
def get_html_tree(target_url):
    # page = requests.get(target_url)
    # return html.fromstring(page.content)
    content = urllib2.urlopen(target_url).read()
    return html.fromstring(content)

def get_leaping_bunny(target_url):
    tree = get_html_tree(target_url)
    root_div = tree.xpath('//div[@id="lb-brands"]/div[2]/div[*]/div/div[*]/div')
    result = []
    for item in root_div:
        name = get_text_from_divs(item.xpath('div[2]/span/a'))
        link = get_text_from_divs(item.xpath('div[3]/span/div/div[2]/div[1]/a'))
        img = get_attr_from_divs(item.xpath('div[1]/div/a/img'), 'data-src')
        result.append([name, link, img])
    return result

#
# Use regular expression to match img url to type. The ordering of reg exp array matters.
# The more complicated matches first.
#
def decide_type_by_img_url(img_url):
    img_url_without_space = img_url.replace('%20', '')
    reg_exps = [['Some Vegan and NZ Made', '.*icon-somevegan.*nz.*made.*.(gif|jpg|png).*'],
                ['Vegan and NZ Made', '.*icon-vegan.*nz.*made.*.(gif|jpg|png).*'],
                ['Some Vegan', '.*icon-somevegan.*.(gif|jpg|png).*'],
                ['Vegan', '.*icon-vegan.*.(gif|jpg|png).*']]
    for reg_exp in reg_exps:
        if re.match(reg_exp[1], img_url_without_space):
            return reg_exp[0]
    return 'Other'

def page_contains_data(target_url):
    content = str(urllib2.urlopen(target_url).read())
    return content.find('Types of product') > 0

def get_safe_shopper(target_url):
    result = []
    for page in range(0, 20):
        print('------ Page is: ' + str(page))
        url = target_url + str(page)
        if page_contains_data(url):
            tree = get_html_tree(url)
            root_div = tree.xpath('//section[@id="block-system-main"]/span/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div[*]')
            for item in root_div:
                name = get_text_from_divs(item.xpath('div[2]/div/a/h4'))
                link = get_attr_from_divs(item.xpath('div[2]/div/a'), 'href')
                type_img_url = get_attr_from_divs(item.xpath('div[1]/div/img'), 'src')
                type = decide_type_by_img_url(type_img_url)
                result.append([name, link, type])
        else:
            break
    return result

items = get_safe_shopper('https://www.safe.org.nz/safeshopper-cruelty-free-nz?page=')
print("-- Safe Shopper, ", len(items) ,"brands -------------------------------------------------------------")
# print (items)
for items in items:
    print(items)


# bunnies = get_leaping_bunny('http://www.leapingbunny.org/guide/brands')
# print("-- Leaping Bunny, ", len(bunnies) ,"brands -------------------------------------------------------------")
# # print (bunnies)
# for items in bunnies:
#     print(items)

