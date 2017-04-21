import re
import requests
import os
import sys
from multiprocessing import Queue,Pool,Manager
# import multiprocessing

def download(url, type):
    # print (url)
    file_name = url.split('/')[-1] + str("." + type)
    r = requests.head(url, headers={'Accept-Encoding': 'identity'})
    response = requests.get(url)
    f = open(file_name, 'wb')
    f.write(response.content)
    # print ("responce.content: " + str(len(response.content)))
    print ("Downloading: " + file_name)  # +" Bytes: "+str(file_size))

    f.close()
    return file_name

def work(input):
    # print (multiprocessing.current_process())
    for link,type in input:
        file_name = download(link, type)
        print ("Downloaded: " + file_name)

def work1(input):
    # print (multiprocessing.current_process())
    link, type = input
    file_name = download(link,type)
    print ("Downloaded: "+file_name)

def foo(input):
    print ("foo: ")
    for i in input:
        print (i)

def foo1(input):
    link, type = input
    print (link,':',type)

if (__name__=="__main__"):
    url = input("WebPage URL: ")
    dir = input("Dir: ")
    currDir = os.getcwd()
    if not os.path.exists(currDir + "\\" + dir):
        os.makedirs(currDir + "\\" + dir)
    os.chdir(currDir + "\\" + dir)
    if (os.path.isfile(url.split('/')[-1] + str(".html"))):
        print ("File Already Exist")
        sys.exit()
    htmlFile = download(url, "html")
    print (htmlFile)
    file = open(htmlFile, "rb")
    out = open("url", 'w+')
    urls = []
    for line in file:
        for match in re.findall('\"size\":2048,\"url\":\".*?\"', line.decode('utf-8'),
                                re.DOTALL):  # re.finditer(r"\"size\":2048,\"url\":\".*?\"",line):
            match = re.sub(r"\\", "", match)
            match = re.sub(r"\"size\":2048,\"url\":", "", match)
            match = re.sub(r"\"", "", match)
            # print (match)
            urls.append((match, "jpg"))
            out.write(match + "\n")
    p = Pool(20)
    p.map(work1,urls)
    p.close()
    p.join()



