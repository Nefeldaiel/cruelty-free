import requests
from lxml import html


def get_leaping_bunny():
    target_url = 'http://www.leapingbunny.org/guide/brands'
    page = requests.get(target_url)
    tree = html.fromstring(page.content)
    divs = tree.xpath('//div[@id="lb-brands"]/div[2]/div[*]/div/div[*]/div/div[2]/span/a')
    return [div.text_content() for div in divs]


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

# bunnies = get_leaping_bunny()
# print("-- Leaping Bunny, ", len(bunnies) ,"brands -------------------------------------------------------------")
# print (bunnies)

frees = get_choose_cruelty_free()
print("-- Choose Cruelty Free, ", len(frees) ,"brands -------------------------------------------------------------")
print(frees)
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
