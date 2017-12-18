from flask import Flask, request
# import requests
from lxml import html
import urllib2
import logging
import ujson


app = Flask(__name__)

def get_leaping_bunny():
    target_url = 'http://www.leapingbunny.org/guide/brands'
    # page = requests.get(target_url)
    # tree = html.fromstring(page.content)
    content = urllib2.urlopen(target_url).read()
    tree = html.fromstring(content)
    divs = tree.xpath('//div[@id="lb-brands"]/div[2]/div[*]/div/div[*]/div/div[2]/span/a')
    return [div.text_content() for div in divs]

@app.route('/')
def hello():
    json = '{ "message" : "Hello World!" }'
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, json)

@app.route('/bunnyget')
def getBunny():
    brand_list = get_leaping_bunny()
    brand_list_str = '<br>'.join(brand_list).encode('utf-8').strip()
    asDict = {'message': brand_list_str}
    json = ujson.dumps(asDict)
    callback = request.args.get('callback')
    return '{0}({1})'.format(callback, json)
    # return json

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

