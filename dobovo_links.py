import requests
import lxml.html as html
import ast

links = set()

def parse_links():
    url = 'https://www.dobovo.com'
    ajax = 'https://www.dobovo.com/dobovo/home/ajax.php?action=getCityCards&lang=en'
    next_btn = '1'

    r_id = requests.get(url)
    tree_id = html.fromstring(r_id.content)
    onclick = tree_id.xpath('.//button[@class = "load-more"]//@onclick')
    more_id = onclick[0][-10:-1]
    list_id = [1,8,3] + ast.literal_eval(more_id)
    j = 0

    for i in list_id:
        id_ = i
        params = {
            'id': str(i),
            'show_next_btn': next_btn
            }
        r = requests.post(url=ajax, data=params)
        data = r.json()['html']
        tree = html.fromstring(data)
        a = tree.xpath('.//a[@class = "item__title"]//@href')

        for item in a:
            links.add(item)
            
        if j > 2:
            onclick = tree.xpath('.//button[@class = "load-more"]//@onclick')
            #try:
            if onclick:
                more_id = onclick[0][21:-1]
                list_more_id = ast.literal_eval(more_id
                                                )
                for x in list_more_id:
                    if x not in list_id:
                        list_id.append(x)    
        j += 1 
    with open('links%s.txt' % str(len(links)) , 'w') as file:
        for item in links: 
            file.write(item + '\n',)
        


