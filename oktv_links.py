import requests
from lxml import html
import json

all_links = []
main = 'https://oktv.ua/search?'

def get_links():      
    for i in range(1,200):
        page = 'page=' + str(i)
        url_ = main + page
        
        if i == 1:
            url_ = main
        
        r = requests.get(url=url_)
        content = r.text
        #print(content)
        tree = html.fromstring(content)
        links = tree.xpath('.//div[@class = "col-xs-12 bl_1"]//@href')
        if links:
            links = [x for x in links if x != '#' ]
            for link in links:
                if link not in all_links:      
                    all_links.append(link)

            #all_links += links
            #print(links, '\n')
            #print('len = ', len(all_links))
        else:
            break

    length = len(all_links)

    with open('oktv_links%s.txt' % str(length), 'w') as f:
        for link in all_links:
            f.write(link + '\n')


   
