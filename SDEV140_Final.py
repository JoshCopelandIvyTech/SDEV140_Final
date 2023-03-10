#start of the final working on downloading imgs using beautifulSoup
from urllib.request import urlopen, build_opener, install_opener
from urllib.parse import urlparse
from PIL import Image
from tkinter.filedialog import asksaveasfilename
import re
import PySimpleGUI as psg
from bs4 import BeautifulSoup
from os.path import basename

class ImgScraper:
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)
    imgTable = []
    imgDataList = []
    baseURL = None
    def getImg(self, URL):
        self.imgDataList.clear()
        self.imgTable.clear()
        parse = urlparse(URL)
        ImgScraper.baseURL = f"{parse.scheme}://{parse.netloc}"
        htmlData = BeautifulSoup(urlopen(URL), "html.parser")
        htmlImgs = htmlData.find_all("img")
        print(htmlImgs)
        self.getImgInfo(htmlImgs)

    def getImgName(self, item):
        print("src", item['src'])
        name = re.split("[.]{1}[a-z]{3,4}\Z", basename(urlparse(item['src']).path))[0]
        # print(name)
        i = 0
        newName = name
        while(True):
            # print(newName)
            i+=1
            if not any(newName in item for item in self.imgDataList):
                return newName
            else:
                newName = name
                newName+=str(i)
            
    def getImgInfo(self, htmlImgs):
        size = len(htmlImgs)-1
        print(size)
        count = 0
        for item in htmlImgs:
            count+=1
            # print(item)
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
                name = self.getImgName(item)
                imgRow = [name, imgType, imgRes]
                ImgScraper.imgTable.append(imgRow)
                imgData = (name, data)
                self.imgDataList.append(imgData)
            if not psg.one_line_progress_meter("loading", count, size, "images"):
                    break
            
class GUI(ImgScraper):
    URLselect = None
    imgSelect = None
    loadingPopUp = None
    window = None
    event= None
    value= None
    rowSelected = 0
    fileName = None
    fileType = None
    
    def URLwindow(self):
        print("URLwind")
        layout = [
        [psg.Text("Enter URL to open "), 
         psg.Input(key="-URL-"), 
         psg.Open()
        ]
        ]
        return psg.Window("URL Input", layout, size=(550, 50), resizable=True, finalize=True)
    
    def imgSelectWindow(self):
        tableHeadings = ["Name", "Type", "Resolution"]
        layout = [
            [psg.Table(values=super().imgTable, headings= tableHeadings, auto_size_columns=True,enable_click_events=True,key="-Table-", expand_x=True, expand_y=True)],
            [psg.Text("Select a Image",key="-ImgSelect-"), 
             psg.Button("Save", key="-SaveTest-"), 
             psg.Button("View", key="-ImgView-")
            ]
        ]  
        return psg.Window("Img Browser", layout, size=(550, 500), resizable=True, finalize=True)
    
    def openURL(self):
        print(self.values["-URL-"])
        try:
            super().getImg(self.values["-URL-"])
        except(Exception) as er:
            print(">>>>>>", er)
            psg.popup(er)
        else:
            if super().imgTable:
                self.URLselect.hide()
                self.imgSelect = self.imgSelectWindow()
            else: 
                psg.popup("No valid images found.")
    
        
    def pickImg(self):
        # print(">>>>", self.event, self.values)
        self.rowSelected = self.event[2][0]
        self.fileName = super().imgTable[self.event[2][0]][0]
        print(self.fileName)
        self.fileType = super().imgTable[self.event[2][0]][1]
        print(self.fileType)
        self.window["-ImgSelect-"].update(self.fileName)
        
    def showImg(self):
        print(self.rowSelected)
        super().imgDataList[self.rowSelected][1].show()
        # psg.popup_no_buttons(image=super().imgDataList[2][1])    
        
    def saveImg(self):
        saveTest = asksaveasfilename( initialfile= self.fileName)
        saveTest+= f".{self.fileType}"
        print(saveTest)
        super().imgDataList[self.rowSelected][1].save(saveTest)
        
    def closeWindow(self):
        self.window.close()
        if self.window == self.imgSelect:
            self.imgSelect = None
            self.URLselect.UnHide()
        elif self.window == self.URLselect:
            return True
    
    def listen(self):
        self.URLselect = self.URLwindow()
        print(self.URLselect, self.imgSelect)
        while True:
            self.window, self.event, self.values = psg.read_all_windows() 
            print(self.window, self.event, self.values)
            if self.event == psg.WIN_CLOSED:
                if self.closeWindow():
                    break
            if self.event == "Open":
                self.openURL()
            if self.event != None and "+CLICKED+" in self.event and self.event[2][0] != None:
                self.pickImg()
            if self.event == "-ImgView-":
                self.showImg()
            if self.event == "-SaveTest-":
                self.saveImg()
        self.window.close()



gui = GUI()
gui.listen()


