from flask import Flask, request
## import requests
from lxml import html
import urllib2
import logging
import ujson
import re


app = Flask(__name__)

empty_string = '-'

def get_text_from_divs(divs):
    if len(divs) > 0:
        return divs[0].text_content()
    return empty_string

def get_attr_from_divs(divs, attr_name):
    if len(divs) > 0:
        return divs[0].get(attr_name)
    return empty_string

#
# Different implementation between using "requests" and "urllib2" (python 2.7 pre-installed)
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
        url = get_text_from_divs(item.xpath('div[3]/span/div/div[2]/div[1]/a'))
        img = get_attr_from_divs(item.xpath('div[1]/div/a/img'), 'data-src')
        # combination = '{} {} <img src="{}">'.format(name, url, img)
        combination = name + ' (<a href="' + url + '" >' + url + '</a>) <img src="' + img + '" >'
        result.append(combination)
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

def page_contains_data(target_url, key):
    try:
        content = str(urllib2.urlopen(target_url).read())
        return content.find(key) > 0
    except:
        return False

def get_safe_shopper(target_url):
    result = []
    for page in range(0, 20):
        print('------ Page is: ' + str(page))
        url = target_url + str(page)
        if page_contains_data(url, 'Types of product'):
            tree = get_html_tree(url)
            root_div = tree.xpath('//section[@id="block-system-main"]/span/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div[*]')
            for item in root_div:
                name = get_text_from_divs(item.xpath('div[2]/div/a/h4'))
                link = get_attr_from_divs(item.xpath('div[2]/div/a'), 'href')
                type_img_url = get_attr_from_divs(item.xpath('div[1]/div/img'), 'src')
                type = decide_type_by_img_url(type_img_url)
                # result.append([name, link, type])
                combination = name + ' (<a href="' + link + '" >' + link + '</a>) ' + type
                result.append(combination)
        else:
            break
    return result

def can_use_rabbit_logo(class_str):
    return str(class_str).find('pink') > -1

def parse_type_from_name(name_str):
    predefined_types = ['v', 'sv', 'vt', 'bp', 'CPOF']
    types = []
    splits = str(name_str).split()
    for item in splits:
        if item in predefined_types:
            types.append(item)
            predefined_types.remove(item)
    return types


def parse_type_and_name(name_str):
    predefined_types = ['v', 'sv', 'vt', 'bp', 'CPOF']
    types = []
    name = name_str.strip()
    try:
        splits = name.split()
        for item in splits:
            if item in predefined_types:
                types.append(item)
                predefined_types.remove(item)
                splits.remove(item)
                name = ' '.join(splits)
    except:
        print('Fail to split ' + name)
    return name, types

def get_choose_cruelty_free(target_url):
    result = []
    tree = get_html_tree(target_url)
    name_divs = tree.xpath('//*[@id="main"]/div/div[2]/article[*]/h2/a')
    for name_div in name_divs:
        name, type = parse_type_and_name(name_div.text_content())
        class_str = name_div.get('class')
        rabbit = can_use_rabbit_logo(class_str)
        index = name_div.get('href')
        index = str(index).replace('#', '')
        link_div = tree.xpath('//*[@id="' + index + '"]/div/div[1]/*/a')
        link = get_attr_from_divs(link_div, 'href')
        # result.append([name, rabbit, link, type])
        combination = name + ' (<a href="' + link + '" >' + link + '</a>), Rabbit Logo: ' + str(rabbit) + ' , type: ' + (', '.join(type))
        result.append(combination)
    return result


def generate_formatted_for_weebly(brand_list):
    brand_list_str = '<br>'.join(brand_list).strip()
    asDict = {'message': brand_list_str}
    json = ujson.dumps(asDict)
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, json)
    # try:
    #     ret = get_leaping_bunny()
    # except:
    #     print "Unexpected error at bunnyget: ", sys.exec_info()[0]
    #     ret = ''
    # return ret

@app.route('/')
def hello():
    json = '{ "message" : "Hello World!" }'
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, json)


@app.route('/getleapingbunny')
def getBunny():
    brand_list = get_leaping_bunny('http://www.leapingbunny.org/guide/brands')
    return generate_formatted_for_weebly(brand_list)


@app.route('/getsafeshopper')
def getSafeShopper():
    brand_list = get_safe_shopper('https://www.safe.org.nz/safeshopper-cruelty-free-nz?page=')
    return generate_formatted_for_weebly(brand_list)

@app.route('/getchoosecrueltyfree')
def getChooseCrueltyFree():
    brand_list = get_choose_cruelty_free('https://choosecrueltyfree.org.au/lists/choose-cruelty-free-list/')
    return generate_formatted_for_weebly(brand_list)

@app.route('/listtask')
def listTask():
    print("task")
    # client = create_client(args.project_id)
    # return list_command(client)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# print get_leaping_bunny()

