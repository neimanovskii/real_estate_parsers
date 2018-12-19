import requests
from lxml import html
import datetime
import json
import oktv_links

def oktv_parse(id_link, app_file):
    main = 'https://oktv.ua'
    ajax = main + id_link
    publicAction_ = 'calendar'
    id_ = [ajax]
    point_ = '1506805200'
    params = {
        'publicAction': publicAction_,
        'id': id_,
        'point' : point_         
        }
    r = requests.post(url=ajax, data=params)
    content = r.text
    tree = html.fromstring(content)

    dates = tree.xpath('.//div[@class = "num"]')
    prices = tree.xpath('.//div[@class = "price"]')
    availables = tree.xpath('.//div[@class = "calendar"]/div/@class')
    months = tree.xpath('.//div[@class = "title_month"]')

    j = 0
    
    for date, available, price in zip(dates,availables, prices):
        if date.text_content() == '1' :
            if j < 2: 
               app_file.write(months[j].text_content() + '\n')
            j +=1
            
        if available == 'day ': 
            app_file.write('day:%s,' % date.text_content().replace("\n", "") + 'price:' + price.text_content().strip() + '\n')
        else:
            app_file.write('day:%s,' % date.text_content().lstrip() + "not available" + '\n')

if __name__ == '__main__':
    print('waint a few minutes')
    print('links parsing...')
    
    oktv_links.get_links()
    
    f = open('oktv_links%s.txt' % len(oktv_links.all_links), 'r')
    
    print("files creating...")
    for id_ in f:
        valid_id = id_.replace('\n', "")
        file_name = valid_id[1:]
        print(file_name)
        app_file = open(file_name + '.txt', 'w')
        oktv_parse(id_, app_file)
        app_file.close()
        print("file was creating.")
        
        


