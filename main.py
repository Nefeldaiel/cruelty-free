import requests
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

def get_leaping_bunny():
    # target_url = '/Users/CYLIU/Programming/Python/cruelty-free/crawler/test-data/LeapingBunny.htm'
    target_url = 'http://www.leapingbunny.org/guide/brands'
    page = requests.get(target_url)
    tree = html.fromstring(page.content)
    root_div = tree.xpath('//div[@id="lb-brands"]/div[2]/div[*]/div/div[*]/div')
    result = []
    for item in root_div:
        name = get_text_from_divs(item.xpath('div[2]/span/a'))
        url = get_text_from_divs(item.xpath('div[3]/span/div/div[2]/div[1]/a'))
        img = get_attr_from_divs(item.xpath('div[1]/div/a/img'), 'data-src')
        result.append([name, url, img])
    return result

def get_choose_cruelty_free():
    target_url = 'http://www.choosecrueltyfree.org.au/cruelty-free-list/'
    page = requests.get(target_url)
    tree = html.fromstring(page.content)
    divs = tree.xpath('//div[@id="post-8"]/div[2]/div[*]/h4//a')
    return [div.text_content() for div in divs]

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

bunnies = get_leaping_bunny()
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
