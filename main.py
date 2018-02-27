# import requests
import urllib2
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
        url = get_text_from_divs(item.xpath('div[3]/span/div/div[2]/div[1]/a'))
        img = get_attr_from_divs(item.xpath('div[1]/div/a/img'), 'data-src')
        result.append([name, url, img])
    return result

# def get_choose_cruelty_free():
#     target_url = 'http://www.choosecrueltyfree.org.au/cruelty-free-list/'
#     page = requests.get(target_url)
#     tree = html.fromstring(page.content)
#     divs = tree.xpath('//div[@id="post-8"]/div[2]/div[*]/h4//a')
#     return [div.text_content() for div in divs]

    # divs = tree.xpath('//div[@id="post-8"]/div[2]/div[67]/h4//a/span[0]/text()');
    # divs = tree.xpath('//div[@id="post-8"]/div[2]/div[68]/h4//a')[0]
    # print(divs.text_content())
    # divs = tree.xpath('//div[@id="post-8"]/div[2]/div[1]/h4//a')[0]
    # print(divs.text_content())
    # return ""


# divs = tree.xpath('//div[@id="post-8"]/div[2]/div[*]/h4//a/text()')
# print(divs)
# return divs;
# //div[@id="post-8"]/div[2]/div[1]/h4/a
# //div[@id="post-8"]/div[2]/div[2]/h4/span/a

bunnies = get_leaping_bunny('http://www.leapingbunny.org/guide/brands')
print("-- Leaping Bunny, ", len(bunnies) ,"brands -------------------------------------------------------------")
# print (bunnies)
for items in bunnies:
    print(items)


# frees = get_choose_cruelty_free()
# print("-- Choose Cruelty Free, ", len(frees) ,"brands -------------------------------------------------------------")
# print(frees)
# for free in frees:
# 	print(free.text_content())


# #sauce = urllib.request.urlopen(targetUrl).read()
# #soup = bs.BeautifulSoup(sauce, 'lxml')
# #print(soup.title)

# with open("LeapingBunny.htm") as fp:
#     soup = bs.BeautifulSoup(fp, 'lxml')

# //*[@id="lb-brands"]/div[2]/div[1]/div/div[1]/div/div[2]/span/a
# //*[@id="lb-brands"]/div[2]/div[1]/div/div[2]/div/div[2]/span/a
# //*[@id="lb-brands"]/div[2]/div[2]/div/div[1]/div/div[2]/span/a

# print(soup.title)

# brands = soup.find('div', id='lb-brands')
