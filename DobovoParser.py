import requests
import timeit
from datetime import date
from lxml import html
import dobovo_links


def get_name(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    flat_view = tree.xpath('.//div[@class = "flat-promo"]/h1/text()')[0]
    flat_adress = tree.xpath('.//div[@class = "address dbv_js_aptaddress"]')[0].text_content()
    print(flat_view.strip(), '\n',
           flat_adress.strip())         


def get_calendar(id):
    ajax = 'https://www.dobovo.com/dobovo/apt/ajax.php?action=getCalendar&lang=en'
    first_day_in_month = date.today()
    id_ = id
    form_data = {
        'id': id_,
        'date': first_day_in_month
    }
    r = requests.post(url=ajax, data=form_data)
    return r.json()
    
def page_parse(response, f):
    f.write('first month:' + response['first_month'] +
            '\nlast month:'+ response['last_month'])
    
    for date in response['calendar']:
        f.write(date)#, end=' ')
        if response['calendar'][date]['state'] == '1':
            f.write('price:' + response['calendar'][date]['price'] +  response['calendar'][date]['currency'] + '\n')
        else:
            f.write('Appartments is not available\n')
    
        
if __name__ == '__main__':
    print('waint a few seconds')
    print('links parsing...')
    dobovo_links.parse_links()
    links_file = open('links%s.txt' % str(len(dobovo_links.links)), 'r')
    print('files creating...')
    for url in links_file:
        valid_url = url.strip('\n')
        id = valid_url[-39:-33]
        '''
           get name
    '''
        page = requests.get(valid_url)
        tree = html.fromstring(page.content)
        flat_view = tree.xpath('.//div[@class = "flat-promo"]/h1/text()')[0]
        flat_adress = tree.xpath('.//div[@class = "address dbv_js_aptaddress"]')[0].text_content()

        valid_name = flat_adress.replace(' ','').replace(',','').replace('\n','').replace('/', '_')
        f = open( valid_name + '.txt', 'w')
        f.write(flat_view.strip() + '\n' +
               flat_adress.strip())
        
        #get_name(valid_url)
        response = get_calendar(id)
        page_parse(response, f)
        f.close()

            
