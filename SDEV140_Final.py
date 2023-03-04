#start of the final working on downloading imgs using beautifulSoup
from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener
from urllib.parse import urlparse
from abc import ABC, abstractmethod
import html5lib
import re
import PySimpleGUI as psg
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from os.path import basename, isfile

# url = "https://www.google.com/search?q=mech&tbm=isch&ved=2ahUKEwid1an80q79AhVD5skDHbdoDogQ2-cCegQIABAA&oq=mech&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIECAAQQzIHCAAQsQMQQzIICAAQgAQQsQMyBAgAEEMyBAgAEEMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDOgQIIxAnOgoIABCxAxCDARBDOgUIABCABDoHCCMQ6gIQJ1D0HFiDaWCrbGgEcAB4AIABUIgBgQSSAQE5mAEAoAEBqgELZ3dzLXdpei1pbWewAQrAAQE&sclient=img&ei=Le_4Y92KCMPMp84Pt9G5wAg&bih=950&biw=1920&rlz=1C1CHBF_enUS1042US1042"
# url2 = "https://unsplash.com/s/photos/car"
# # htmlReq = Request(url, headers={'User-Agent': 'Mozilla/5.0'}     )
# # htmlData = urlopen(htmlReq)
# opener = build_opener()
# opener.addheaders = [('User-agent', 'Mozilla/5.0')]
# install_opener(opener)
# htmlData = urlopen(url2)
# # print(htmlReq, htmlData)
# soup = BeautifulSoup(htmlData, 'html.parser')
# # diagnose(soup)
# # print(soup)
# images = soup.find_all('img')
# # print(images)
# count = 0
# for item in images:
#     print(count)
#     if count >= 30:
#         break
#     count+=1
#     try:
#         # print(item)
#         # print(item['src'])
#         path = item['src']
#         name = basename(urlparse(item['src']).path)
#     except(AttributeError, KeyError) as er:
#         pass
#     print(path, name)
#     print(">>>>>")
#     try:
#         imgData = urlopen(path)
#         print(imgData.info())
#         imgType = imgData.info()["Content-Type"].split("/")[-1]
#         # print(imgType)
#     except(ValueError) as er:
#         print(f"Bad url: {path}")
#         imgType = False
#     extensionSearch = re.search("[.]{1}[a-z]{3,4}\Z", name)
#     if not extensionSearch and imgType:
#         print("<<<<<")
#         # print(extensionSearch, imgType)
#         # imgType.strip("image/")
#         # name = name+f".{imgType}"
#         # print(name)
    
#     if(imgType):
#         if not isfile(f"../Final/img/{name}.{imgType}"):
#             print("...")
#             img = open(f"../Final/img/{name}.{imgType}", "wb")
#             img.write(imgData.read())
#             img.close()
#         else:
#             fileCount = 1
#             while(isfile(f"../Final/img/{name}{str(fileCount)}.{imgType}")):
#                 # print("???", fileCount)
#                 fileCount+=1
#             img = open(f"../Final/img/{name}{str(fileCount)}.{imgType}", "wb")
#             img.write(imgData.read())
#             img.close()
#             print(fileCount)
# print(urlopen(url).info())

class URLwindow:
    layout = [
        [psg.Text("Enter URL to open "), psg.Input(key="-URL-"), psg.Open()]
    ]
    window = psg.Window("URL Input", layout, size=(550, 50), resizable=True)
    def listen(self):
        while True:
            event, values = URLwindow.window.read() 
            print(event)
            if event == psg.WIN_CLOSED:
                break
            if event == "Open":
                print(values["-URL-"])

class ImgSelect:
    layout = [
        [psg.Text("Enter URL to open "), psg.Input(key="-URL-"), psg.Open()]
    ]  

# URL = URLwindow()
# URL.listen()

