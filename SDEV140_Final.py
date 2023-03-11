#start of the final working on downloading imgs using beautifulSoup
from urllib.request import urlopen, build_opener, install_opener
from urllib.parse import urlparse
from PIL import Image, ImageShow
from tkinter.filedialog import asksaveasfilename
import re
import PySimpleGUI as psg
from bs4 import BeautifulSoup
from os.path import basename

# class for containing need scraping methods and data is parent class of GUI class
class ImgScraper:
    # creates a opener to be used for urlopen requests 
    opener = build_opener() #gets an opener instance
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] # adds user-agent header to our opener to help trick websites into thinking our request is from a real user
    install_opener(opener) # makes our opener the default opener for our program
    # class vaiiables 
    imgTable = [] # for storing a tuple of our image data used to make our img picker table (name, fileType, resolution)
    imgDataList = [] # for storing a tuple holding the img name and a pillow image object
    baseURL = None # used for storing the base url of the website we are sracping to be used if a img src doesn't have one.
    def getImg(self, URL): # gets opens the URL and get its html data then searchs for img tags
        # makes sure that both imgDataList and imgTable are cleared when opening a new page so that no old img are mix with new ones
        self.imgDataList.clear()
        self.imgTable.clear()
        
        #parse to get the base URL
        parse = urlparse(URL)
        ImgScraper.baseURL = f"{parse.scheme}://{parse.netloc}"
        
        # Gets URL HTML data and parses it then makes a list of its img tags then passes them to getImgInfo function
        htmlData = BeautifulSoup(urlopen(URL), "html.parser")
        htmlImgs = htmlData.find_all("img")
        # print(htmlImgs)
        self.getImgInfo(htmlImgs)

    # takes a img tag then creates a name for the img using its src
    def getImgName(self, item):
        # print("src", item['src'])
        #uses urlparse to get file path from src then use os.path basename of the path then finaly uses regEx to split any file extension for it
        name = re.split("[.]{1}[a-z]{3,4}\Z", basename(urlparse(item['src']).path))[0]
        # print(name)
        #count number of passes of the while loop
        i = 0
        # copy of name to be modiifed inside the while loop
        newName = name
        # will search through imgDataList if any imgs already have newName and if they do will keep adding a different number to the end untill they aren't
        while(True):
            # print(newName)
            # increase i by 1
            i+=1
            # checks if newName is not already taken
            if not any(newName in item for item in self.imgDataList):
                return newName
            # if not then rest newName back then add i to its end
            else:
                newName = name
                newName+=str(i)
            
    # will try to download the img using its src and make a Pillow image object from it. Then get add it to both imgTable and imgDataList
    def getImgInfo(self, htmlImgs):
        #get the amount of imgs tags to use for a progress bar pop up
        size = len(htmlImgs)-1
        # print(size)
        # to count how many imgs have be processed
        count = 0 
        # loops through img tags 
        for item in htmlImgs:
            count+=1
            # print(item)
            # local variables 
            path = item['src'] # stores img's src
            data = None #stores Pillow image object
            name = None #stores img name from getImgName
            # main try block for catching any expceptions made trying to save img to memory 
            try:
                # try block to see if src is a proper URL
                try:
                    # print(path)
                    #saves img data to data as a image object
                    data = Image.open(urlopen(path))
                # if URL is not vaild trys to add websit's base URL to the beginning of it
                except(ValueError):
                    print("<<<<")
                    path = ImgScraper.baseURL+'/'+item['src']
                    # print(path)
                    data = Image.open(urlopen(path))
            # if still can't save img to memory then print error and do nothing with it
            except(Exception) as er:
                print(">>>", er)
            # if img was saved to memory then create a 2 new tuples to be added to imgTable and imgDataList
            else:
                # get img name using getImgName function
                name = self.getImgName(item)
                # create tuple to be added to imgTable
                imgRow = (name, data.format, data.size)
                self.imgTable.append(imgRow)
                #create tuple to be added to imgDataList
                imgData = (name, data)
                self.imgDataList.append(imgData)
            # create a progress bar popup to update tell the user how the img processing is going and allow them to stop it. had to be with in the loop that it was monitor to work or else would be in GUI class
            if not psg.one_line_progress_meter("loading", count, size, "images loaded"):
                    break

# class for containing all need methods and data need for the GUI is child class of ImgScraper class        
class GUI(ImgScraper):
    # class variables
    URLselect = None # use to hold an instance of URLwindow
    imgSelect = None # use to hold an instance of ImgSelectWindow
    window = None # stores the window object that is firing an event
    event= None # stores the event tuple
    value= None # stores the value of the element of the current event
    rowSelected = 0 # stores the row number that was selected from the table in img select window
    fileName = None # stores the name of the currently selected file 
    fileType = None # stores the file type of the currently selected file
    
    # create a window object for inputing URL
    def URLwindow(self):
        print("URLwind")
        # a list that repersents window layout 
        layout = [
        [psg.Text("Enter URL to open "), # a lable element 
         psg.Input(key="-URL-"), # text input element used to get URLselect
         psg.Open() # open button fires an OPEN event to tell program to open a img select window
        ]
        ]
        # create and returns a window object
        return psg.Window("URL Input", #windows name 
                          layout, # its layout 
                          size=(550, 50), #its size in pixels 
                          resizable=True, # allows user to resize it 
                          finalize=True # tells program to open window when created
                        )
    
    # create window object for selecting an img and choosing what to do with it
    def imgSelectWindow(self):
        tableHeadings = ["Name", "Type", "Resolution"] # labels to be used for table columns
        layout = [
            # a table element to display imgTable data
            [psg.Table(values=super().imgTable, # uses imgTable to create its rows
                       headings= tableHeadings, # uses tableHeadings to create its column's labels
                       auto_size_columns=True, # tells program to auto size columns
                       enable_click_events=True, # tells program to fire a event when table is clicked giving the number of the row and column clicked
                       key="-Table-", # used to refer to this element
                       expand_x=True, # tells program to expand this table width to fit window
                       expand_y=True) # tells program to expand this table height to fit window
            ],
            [psg.Text("Select a Image",key="-ImgSelect-"), # label that starts as Select a Image but then will change to the name of the selected img
             psg.Button("Save", key="-SaveTest-"), # a save button that fires a -SaveTest- event
             psg.Button("View", key="-ImgView-") # a view button that fires a -ImgView- event
            ]
        ]  
        # create a window and returns it
        return psg.Window("Img Browser", layout, size=(550, 500), resizable=True, finalize=True)
    
    # is call when an OPEN event is called. takes inputed URL and passes it to getImg then hides URL select window
    def openURL(self):
        print(self.values["-URL-"])
        # try to open URL if it fails then bring up a popup with error message
        try:
            super().getImg(self.values["-URL-"])
        except(Exception) as er:
            print(">>>>>>", er)
            psg.popup(er)
        else:
            # check if imgTable is empty 
            if super().imgTable:
                # hides URL Select window and opens Img Select Window
                self.URLselect.hide()
                self.imgSelect = self.imgSelectWindow()
            # if imgTable is empty then open popup
            else: 
                psg.popup("No valid images found.")
    
    # if a table row is click call this function. will get selected img's name and file type and updates imgSelect text with file name    
    def pickImg(self):
        # print(">>>>", self.event, self.values)
        self.rowSelected = self.event[2][0] # gets selected row
        # print(self.rowSelected)
        self.fileName = super().imgTable[self.rowSelected][0] #gets name from select row 
        # print(self.fileName)
        self.fileType = super().imgTable[self.rowSelected][1] #gets file type from select row
        # print(self.fileType)
        self.window["-ImgSelect-"].update(self.fileName) # updates imgSelect text to file's name
    
    # is called when show button is pressed will show the img   
    def showImg(self):
        print(self.rowSelected)
        # gets image object from imgDataList and shows using an image viewing app
        ImageShow.show(super().imgDataList[self.rowSelected][1])
 
    # is called when save button is pressed and will bring up a file browser save image
    def saveImg(self):
        #opens file browser with fileName as the default name returns a file path
        saveTest = asksaveasfilename( initialfile= self.fileName) 
        # checks if a file path was selected before trying to save img
        if saveTest !='':
            #adds file extension to the end of file path
            saveTest+= f".{self.fileType}"
            print(saveTest)
            #saves the file to file path
            super().imgDataList[self.rowSelected][1].save(saveTest)
        
    # is called if a window is closed/ if it was the img select window then close it and unhide URL select window. If it was URL select window then exit program
    def closeWindow(self):
        # closes window that event was called from
        self.window.close()
        # gets rid of the instance of img select window and un hides URL select window
        if self.window == self.imgSelect:
            self.imgSelect = None
            self.URLselect.UnHide()
        #return True to tell program to break listing loop
        elif self.window == self.URLselect:
            return True
    
    # create a instance of the URL select window and creates a inf loop to listen for events
    def listen(self):
        self.URLselect = self.URLwindow()
        # print(self.URLselect, self.imgSelect)
        while True:
            #will ask all open windows if a any event is happening and returns a which window, event, and value of event element
            self.window, self.event, self.values = psg.read_all_windows() 
            print(self.window, self.event, self.values)
            # if user closes a window call closeWindow
            if self.event == psg.WIN_CLOSED:
                if self.closeWindow():
                    break
            #if user opens a URL call openURL
            if self.event == "Open":
                self.openURL()
            #if user clicked on a table row then then call pickImg
            if (self.event != None # checks if event is iterable
                and "+CLICKED+" in self.event #check if table was clicked 
                and self.event[2][0] != None # checks if user is not resizing column
            ):
                self.pickImg()
            #if user click view button then call showImg
            if self.event == "-ImgView-":
                self.showImg()
            #if user click save button then call saveImg
            if self.event == "-SaveTest-":
                self.saveImg()
        #close window
        self.window.close()

#creates instance of GUI class
gui = GUI()
#call for listen method from GUI class
gui.listen()


