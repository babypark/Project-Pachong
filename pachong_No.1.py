# -*- coding:utf-8 -*-

'''
JD price Spider
Track all the JD international SKU and get name and price
output in CSV files
have fun :)
'''

#import module
import re
import urllib.request
import time
import zlib
import csv
import gc


#CSVWriter initial the CSVfiles and write the data
class CSVWriter:
    def __init__(self,fileName):
        self.fileName = fileName
        self.file = open(fileName,'w',encoding = 'utf-8',newline = '')
        self.writer = csv.writer(self.file)
    #write datas
    def writeData(self,seq):
        self.writer.writerow(seq)
    #close the files
    def closes(self):
        self.file.close()

#the spider gets the information from a url and return his data on web
class spider:
    def __init__(self,url = '',decodeType = 'utf-8'):
        #init the data
        self.data = None

        #this url need be input by user first
        self.url = url

        #this set the decode type
        self.decodeType = decodeType

    #clean all the initial parameter to initial situation
    def clear(self):
        self.data = None
        self.url = ''
        self.decodeType = 'utf-8'

    #set URL and decodeType parameters
    def setURL(self,url):
        self.url = url

    def setdecodeType(self,decodeType):
        self.decodeType = decodeType

    #get data and other parameters
    def getData(self):
        return self.data

    def getURL(self):
        return self.url

    def getDecodeType(self):
        return self.decodeType

    #core of the spider
    def run(self):
        tag = 0
        while tag == 0:
            try:
                tag = 1
                data = urllib.request.urlopen(self.url,data = None,timeout = 1).read()
                data = data.decode(self.decodeType)
                self.data = data
            except UnicodeEncodeError:
                temp = re.split('_',self.url)
                url_temp = temp[0]+temp[1]
                for i in temp[2:]:
                    a = urllib.parse.quote(i)
                    url_temp = url_temp+'_'+a
                data = urllib.request.urlopen(url_temp,data = None,timeout = 1).read()
                data = data.decode(self.decodeType)
                self.data = data
            except Exception as e:
                tag = 0
                print('Error: when run run in spider class')
                print(e)
        return data

    def runZlib(self):
        tag = 0
        while tag == 0:
            try:
                tag = 1
                data = urllib.request.urlopen(self.url,data = None,timeout = 1).read()
                data = zlib.decompress(data,16+zlib.MAX_WBITS)
                data = data.decode('gbk')
                self.data = data
            except Exception as e:
                tag = 0
                print('Error: when run runZlib in spider class')
                print(e)
        return data


#snaker get the data from the spider and analysis it, return the useful information
#obeying the rules input by users
class snaker:
    def __init__(self,reStr = '',data = ''):
        #init the re string
        self.reStr = reStr
        #init the result
        self.result = ''
        #init the data
        self.data = data

    #clean all the initial parameter to initial situation
    def clear(self):
        self.reStr = ''
        self.result = ''
        self.data = ''

    #set re string and data parameters
    def setReStr(self,reStr):
        self.reStr = reStr
    def setData(self,data):
        self.data = data

    #get data and other paras
    def getReStr(self):
        return self.reStr
    def getData(self):
        return self.data
    def getResult(self):
        return self.result

    #core of the snaker
    def runSearch(self):
        try:
            self.result = re.search(self.reStr,self.data).group()
            return self.result
        except Exception as e:
            #print('Error: '+self.data)
            #print(self.reStr)
            #print(e)
            return None

    def runFindAll(self):
        try:
            self.result = re.findall(self.reStr,self.data)
            return self.result
        except Exception as e:
            print('Error: when run Findall in snaker class')
            print(e)
            return None

'''
action 1: analysis the homepage
get homepage url and analysis it
return all the category url in a list
'''
#global paras
homepage = 'http://www.jd.hk/'
listPage = []
listCate = []

writer = CSVWriter('test_150807.csv')

#temp paras
GdetailListPage = []
GID = []
Gname = []
Gprice = []
Gcategory = None
Gurl = []
GpriceID = []

def clear():
    global GdetailListPage
    global GID
    global Gname
    global Gprice
    global Gcategory
    global Gurl
    global GpriceID
    
    GID = []
    Gname = []
    Gprice = []
    Gurl = []
    GpriceID = []

def analysisHomepage():
    Spider = spider(homepage)
    data = Spider.runZlib()

    reS = r'(?<=class="p-category J_p-category">).*?(?=fl10-4">)'
    reS2 = r'(?<=<li>).*?(?=</li>)'

    temp_data = re.search(reS,data,re.S).group()
    sub_list_temp = re.findall(reS2,temp_data,re.S)
    
    reStr = r'(?<=<a clstag).*?(?=</a)'
    nameReStr = r'(?<=title=").*?(?=")'
    nameReStr2 = r'(?<=\n\t\t\t\t\t\t).*?(?=</a>)'
    urlReStr = r'(?<=href=").*?(?=")'
    
    Snaker = snaker(reStr,data)
    listTemp = Snaker.runFindAll()
    
    for j in sub_list_temp:
        Snaker.clear()
        Snaker.setReStr(nameReStr2)
        Snaker.setData(j)
        cate = Snaker.runSearch()
        listCate.append(cate)

        Snaker.clear()
        Snaker.setReStr(urlReStr)
        Snaker.setData(j)
        listUrl = Snaker.runSearch()
        listPage.append(listUrl)
    print('analysisHomepage  sub_cate DONE')
    #print(listPage)
    #print(listCate)

    for i in listTemp:
        Snaker.clear()
        Snaker.setReStr(nameReStr)
        Snaker.setData(i)
        cate = Snaker.runSearch()
        listCate.append(cate)

        Snaker.clear()
        Snaker.setReStr(urlReStr)
        Snaker.setData(i)
        listUrl = Snaker.runSearch()
        listPage.append(listUrl)
    print('analysisHomepage  main_cate DONE')

def getDetailListPage(url):
    global GdetailListPage
    global GID
    global Gname
    global Gprice
    global Gcategory
    global Gurl
    global GpriceID
    
    reStr = r'(?<=p-skip"><em>).*?(?=</b>)'
    reStrSearch = r'(?<=page-skip"><em>).*?(?=</em>)'
    reStr2 = r'\d+'

    print('Start getDetailListPage: '+url)
    
    Spider = spider(url)
    data = Spider.run()

    Snaker = snaker(reStr,data)
    data2 = Snaker.runSearch()
    if not data2:
        print('not list page')
        print('url: '+url)
        return False
        Snaker.clear()
        Snaker.setReStr(reStrSearch)
        Snaker.setData(data)
        data2 = Snaker.runSearch()
        if not data2:
            print('url error while getting list&search page SKU number')
            GdetailListPage.append(url)
            return

    Snaker.clear()
    Snaker.setReStr(reStr2)
    Snaker.setData(data2)
    num = Snaker.runSearch()
    
    for i in range(int(num)):
        GdetailListPage.append(url+'&page='+str(i+1))
    print('get list page number DONE')
    return True


def getData():
    global GdetailListPage
    global GID
    global Gname
    global Gprice
    global Gcategory
    global Gurl
    global GpriceID
    
    tag = 0
    reStr = r'(?<=a target="_blank").*?(?=onclick="log)'
    reStrSearch = r'(?<=target="_blank").*?(?=onclick="searchlog)'
    reStrID = r'(?<=http://item.jd.com/).*?(?=.html)'
    reStrName = r'(?<=title=").*?(?=")'

    detailURL = 'http://item.jd.hk/'

    Spider = spider()
    #get every detail page's SKU name and ID
    for i in GdetailListPage:
        Spider.clear()
        Spider.setURL(i)
        data = Spider.run()
        print('analysis DONE  url:  '+i)

        Snaker = snaker(reStr,data)
        data2 = Snaker.runFindAll()
        if not data2:
            print(i+': is not a list page')
            Snaker.setReStr(reStrSearch)
            data2 = Snaker.runFindAll()
            if not data2:
                print('Error: mistake occurs when analysising a detail list page')
                continue

        for j in data2:
            Snaker.clear()
            Snaker.setData(j)
            Snaker.setReStr(reStrID)
            tID = Snaker.runSearch()
            Snaker.setReStr(reStrName)
            tName = Snaker.runSearch()
            if tID and tName:
                if not (tID in GID):
                    GID.append(tID)
                    #print('get name DONE name: '+tName)
                    Gname.append(tName)
                    #print('get url DONE')
                    Gurl.append(detailURL+tID+'.html')
                    #print('get ID name URL DONE: '+tID)

        print('get ID and URL DONE: '+ i)

        #get every detail SKU'S price
        priceURL = 'http://p.3.cn/prices/mgets?&callback=jQuery2864965&my=list_price&type=1&area=1_72_4137_0&skuIds='
        for k in GID:
            priceURL += 'J_'+str(k)+'%2C'
        print(priceURL)
        Spider.clear()
        Spider.setURL(priceURL)
        tag = 0
        while tag == 0:
            tag = 1
            priceData = Spider.run()
            if not priceData:
                tag = 0

        priceReStr = r'(?<=\().*(?=\))'

        Snaker.clear()
        Snaker.setReStr(priceReStr)
        Snaker.setData(priceData)
        priceData = Snaker.runSearch()
        priceData = eval(priceData)
        for l in priceData:
            Gprice.append(l['p'])
            GpriceID.append(l['id'])

        writeData()
        clear()
    clear()
    GdetailListPage = []


def writeData():
    global GdetailListPage
    global GID
    global Gname
    global Gprice
    global Gcategory
    global Gurl
    global GpriceID
    global writer

    temp = []

    print(len(GID))
    #print(len(Gname))
    #print(len(Gprice))
    #print(len(Gurl))
    #print(len(GpriceID))

    #print(GID)
    #print(Gname)
    #print(Gprice)
    #print(Gurl)
    #print(GpriceID)

    for i in range(len(GID)):
        temp.append(GID[i])
        temp.append(Gname[i])
        temp.append(Gprice[i])
        temp.append(Gcategory)
        temp.append(Gurl[i])
        temp.append(GpriceID[i])
        
        writer.writeData(temp)
        temp = []
    print('write data DONE')

def main():
    
    global GdetailListPage
    global GID
    global Gname
    global Gprice
    global Gcategory
    global Gurl
    global GpriceID
    global writer

    time.clock()
    analysisHomepage()
    for i in range(len(listPage)):
        if getDetailListPage(listPage[i+27]):
            Gcategory = listCate[i+27]
            getData()
            Gcategory = None
            print(time.clock())
            gc.collect()
        clear()
        GdetailListPage = []

    writer.close()
        
main()
