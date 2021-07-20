from bs4 import BeautifulSoup
dict1 = {}



def get_tw():
    with open('../Mastodon.html', 'r',encoding='utf-8') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')
        tws = soup.find_all('div', class_='status__wrapper focusable')
        for tw in tws:
            key = tw.text[:tw.text.find('<p')]
            dict1[key]=tw.text[tw.text.find('<p')+3:-4].replace('</p><p>',' ')
    return dict1