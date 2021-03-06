import json,sys,time,datetime
from requests_html import HTML, HTMLSession
from bs4 import BeautifulSoup

to = ['purshoth27@gmail.com','athishpv2525@gmail.com']

path = r'/home/vsts/test/test/'

sys.path.insert(1,r'/home/vsts/test/test/Drive_API/')
from Drive_API import Drive_API

drive = Drive_API()

session = HTMLSession()

while True:
    name, Id = drive.searchFile('gmStat.json')[0]["Name"], drive.searchFile('gmStat.json')[0]['Id']

    drive.download(Id,name)
    
    with open(path+'gmStat.json') as json_read:
        jsData = json.load(json_read)

    startTime = datetime.datetime.now()
    try:
        src = session.get(url='https://steamunlocked.net/all-games/')
    except Exception as err:
        print(err)

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
            sendMail(to,body,Subject=subject,From='Nea <neas.update@gmail.com>')

    if checker:
        with open(path+'gmStat.json','w') as json_write:
            json.dump(jsData,json_write)
        drive.deleteFile(Id)
        drive.upload('gmStat.json',folder_id='1KrdT_908MrdxXkJdhY6yPmGyBTXq5d0U')
    if startTime.hour == 17:
        print('Completed task at',startTime.ctime())
        break
    time.sleep(900)