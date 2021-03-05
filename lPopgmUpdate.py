import json,sys,time,datetime
from requests_html import HTML, HTMLSession
from bs4 import BeautifulSoup

to = ['purshoth27@gmail.com','athishpv2525@gmail.com']

path = r'/home/vsts/test/test'

sys.path.insert(1,r'/home/vsts/test/test/Drive_API')
from Drive_API import Drive_API

drive = Drive_API()

name, Id = drive.searchFile('gmStat.json')[0]["Name"], drive.searchFile('gmStat.json')[0]['Id']

drive.download(name,Id)
    
with open(path+'/gmStat.json') as json_read:
    jsData = json.load(json_read)

session = HTMLSession()

while True:
    startTime = datetime.datetime.now()
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
            sys.path.insert(1,r'/home/vsts/test/test/Gmail_API')

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
        drive.deleteFile('1TiZAwS_7Bs1X3oxBy9fic3JyGUl6VBIB')
        drive.upload(path+'/gmStat.json')
    time.sleep(900)
    if startTime.hour == 22:
        print('Completed task at',startTime.ctime())
        break