#start of the final working on downloading imgs using beautifulSoup
from urllib.request import urlopen, build_opener, install_opener
from urllib.parse import urlparse
from PIL import Image
import re
import PySimpleGUI as psg
from bs4 import BeautifulSoup
from os.path import basename, isfile, getsize
from io import BytesIO

class ImgScraper:
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)
    htmlImgs=[]
    imgTable = []
    imgDataList = []
    baseURL =''
    loadProg = [1,0]
    def getImg(self, URL):
        parse = urlparse(URL)
        ImgScraper.baseURL = f"{parse.scheme}://{parse.netloc}"
        # print(URL, urlparse(URL), ImgScraper.baseURL)
        # try:
        htmlData = BeautifulSoup(urlopen(URL), "html.parser")
        # except(HTTPError) as er:
            # print(er)
        # else:
        ImgScraper.htmlImgs = htmlData.find_all("img")
        size = len(ImgScraper.htmlImgs)
        print(size)
        ImgScraper.loadProg[0] = size

    
    def getImgInfo(self):
        
        count = 0
        for item in ImgScraper.htmlImgs:
            # print(item)
            count+=1
            ImgScraper.loadProg[1] = count
            print(ImgScraper.loadProg)
            imgRow = []
            path = item['src']
            imgType = ''
            imgRes = ''
            data = None
            try:
                try:
                    # print(path)
                    data = Image.open(urlopen(path))
                except(ValueError):
                    print("<<<<")
                    path = ImgScraper.baseURL+'/'+item['src']
                    # print(path)
                    data = Image.open(urlopen(path))
            except(Exception) as er:
                print(">>>", er)
                imgType = "ERROR"
                imgRes= er
            else:
                imgRes = data.size
                imgType = data.format
            finally:
                name = basename(urlparse(item['src']).path)
                imgRow = [name, imgType, imgRes]
                ImgScraper.imgTable.append(imgRow)
                imgData = (name, data)
                self.imgDataList.append(imgData)
                
        
    
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

class GUI(ImgScraper):
    URLselect = None
    imgSelect = None
    loadingPopUp = None
    window = None
    event= None
    value= None
    rowSelected = 0
    fileName = ''
    
    def URLwindow(self):
        print("URLwind")
        layout = [
        [psg.Text("Enter URL to open "), psg.Input(key="-URL-"), psg.Open()]
        ]
        return psg.Window("URL Input", layout, size=(550, 50), resizable=True, finalize=True)
    
    def imgSelectWindow(self):
        tableHeadings = ["Name", "Type", "Resolution"]
        layout = [
            [psg.Table(values=super().imgTable, headings= tableHeadings, auto_size_columns=True,enable_click_events=True,key="-Table-", expand_x=True, expand_y=True)],
            [psg.Text("",key="-ImgSelect-"), psg.SaveAs(target= "-Target-" ,key="-Save-", initial_folder=f"/{self.fileName}" ), psg.Button("View", key="-ImgView-"), psg.Input("", visible=False, key="-Target-", enable_events=True)]
        ]  
        return psg.Window("Img Browser", layout, size=(550, 500), resizable=True, finalize=True)
    
    def openURL(self):
        print(self.values["-URL-"])
        try:
            super().getImg(self.values["-URL-"])
            # psg.one_line_progress_meter("Loading", super().loadProg[1], super().loadProg[0], "Imgs Loaded")
            super().getImgInfo()
        except(Exception) as er:
            print(er)
            psg.popup(er)
        else:
            # loadingPopUp = None
            # self.URLselect.disable()
            self.URLselect.hide()
            self.imgSelect = self.imgSelectWindow()
            
    # def 
        
    def listen(self):
        self.URLselect = self.URLwindow()
        print(self.URLselect, self.imgSelect)
        while True:
            self.window, self.event, self.values = psg.read_all_windows() 
            print(self.window, self.event, self.values)
            if self.event == psg.WIN_CLOSED:
                self.window.close()
                if self.window == self.imgSelect:
                    print("XXXX")
                    self.imgSelect = None
                    # self.URLselect.enable()
                    self.URLselect.UnHide()
                elif self.window == self.URLselect:
                    break
            if self.event == "Open":
                self.openURL()
            if self.event != None and "+CLICKED+" in self.event and self.event[2][0] != None:
                # print(">>>>", self.event, self.values)
                self.rowSelected = self.event[2][0]
                self.fileName = super().imgTable[self.event[2][0]][0]
                self.window["-ImgSelect-"].update(self.fileName)
            if self.event == "-ImgView-":
                print(self.rowSelected)
                super().imgDataList[self.rowSelected][1].show()
                # psg.popup_no_buttons(image=super().imgDataList[2][1])    
            if self.event == "-Target-":
                print(self.values["-Target-"])
        # self.window.close()

class ImgSelect(ImgScraper):
    
    tableHeadings = ["Name", "Type", "Resolution"]
    layout = [
        [psg.Table(values=ImgScraper.imgTable, headings= tableHeadings, auto_size_columns=True,enable_click_events=True,key="-Table-",expand_y=True,expand_x=True)],
        [psg.Text("",key="-ImgSelect-"), psg.SaveAs, psg.Button("View", key="-ImgView-")]
    ]  
    # window = psg.Window("Img Browser", layout, size=(550, 500), resizable=True)
    def listen(self):
        window = psg.Window("Img Browser", ImgSelect.layout, size=(550, 500), resizable=True)
        print("listing")
        while True:
            event, values = window.read() 
            print("event:", event, "values:", values)
            if event == psg.WIN_CLOSED:
                print("closing")
                break
            
        window.close()
        print("done listing")

gui = GUI()
gui.listen()

# img.listen()

