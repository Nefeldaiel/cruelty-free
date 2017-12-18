from flask import Flask
# import requests
from lxml import html
import urllib2
import logging


app = Flask(__name__)

def get_leaping_bunny():
    target_url = 'http://www.leapingbunny.org/guide/brands'
    # page = requests.get(target_url)
    # tree = html.fromstring(page.content)
    content = urllib2.urlopen(target_url).read()
    tree = html.fromstring(content)
    divs = tree.xpath('//div[@id="lb-brands"]/div[2]/div[*]/div/div[*]/div/div[2]/span/a')
    return [div.text_content() for div in divs]

# @app.route('/')
# def hello():
# 	return 'Hello World!'


@app.route('/bunnyget')
def getBunny():
    list = get_leaping_bunny()
    str = ''.join(list).encode('utf-8').strip()
    return str
    # try:
    #     ret = get_leaping_bunny()
    # except:
    #     print "Unexpected error at bunnyget: ", sys.exec_info()[0]
    #     ret = ''
    # return ret

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# print get_leaping_bunny()

