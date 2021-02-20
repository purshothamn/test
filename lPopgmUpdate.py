import json,sys
from requests_html import HTML, HTMLSession
from bs4 import BeautifulSoup

to = ['purshoth27@gmail.com','athishpv2525@gmail.com']

path = r'/sdcard/Scripts/Python/anime_webScrapping/lPopGmUpdate'
    
with open(path+'/gmStat.json') as json_read:
    jsData = json.load(json_read)

session = HTMLSession()

src = session.get(url='https://steamunlocked.net/all-games/')

soup = BeautifulSoup(src.content, 'lxml')

sol = soup.find_all('div',attrs={'class':"info"})

solList = []

checker = None
for s in sol:
    i = s.find('a').text.replace('\n','').replace('\t','').replace('’','')
# for i in solList:
    if i in jsData['Name']:
        pass
    else:
        checker = True
        sys.path.insert(1,r'/sdcard/Scripts/Python/Google_API/Gmail-API-project/Gmail_API_scripts')

        from Gmail_API import Gmail_API
        sendMail = Gmail_API.createMail

        jsData['Name'].insert(0,i)
        link = s.find('a').attrs['href']
        body = f'{i} is added to Popular, here\'s the link: {link}'
        subject = 'New Popular Game'
        sendMail(to,body,Subject=subject)

if checker:
    with open(path+'/gmStat.json','w') as json_write:
        json.dump(jsData,json_write)