from nltk.tokenize import word_tokenize
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from bs4 import BeautifulSoup
from functools import reduce
import urllib.request
import pandas as pd
import numpy as np
import requests
import string
import heapq
import json
import nltk
import lxml
import bs4
import os


#1.1

def pull_out(url1,url2,URL):
    with open("Pages.txt","w")as f:
        for i in range(1,401):
            if i==1:
                results=requests.get(URL)
                soup =BeautifulSoup(results.text,"lxml")
                for item in soup.find_all('a',{'class':'content-card content-card-place'}):
                     f.write("https://www.atlasobscura.com"+item["href"]+"\n")
            else:
                i=str(i)
                url = url1+i+url2
                results = requests.get(url)
                soup = BeautifulSoup(results.text,"lxml")
                for item in soup.find_all('a',{'class':'content-card content-card-place'}):
                    f.write("https://www.atlasobscura.com"+item["href"]+"\n")

                    

#1.3

def addr(soup):
    Address=soup.find('address',class_='DDPageSiderail__address').div.contents 
    placeAddress=""
    for _ in Address:
        if type(_)==bs4.element.NavigableString:
             placeAddress=placeAddress+" "+_    

    return(placeAddress.replace("\n"," "))


def alt(soup):
    LA=soup.find_all('div',class_='DDPageSiderail__coordinates js-copy-coordinates')[0].text.split()
    placeAlt=LA[0]
    
    return placeAlt


def long(soup):
    LA=soup.find_all('div',class_='DDPageSiderail__coordinates js-copy-coordinates')[0].text.split()
    placeLong=(LA[1])
    
    return placeLong


def DFBuilder():
    placeName = []
    placeTags = []
    numPeopleVisited = []
    numPeopleWant = []
    placeDesc = []
    placeShortDesc = []
    placeNearby = []
    placeAddress = []
    placeAlt = []
    placeLong = []
    placeEditors = []
    placePubDate = []
    placeUrl = []
    k=1
    for i in range(1,401):
        path = os.getcwd()
        directory = "\\Data\\Page"+str(int(i))+"\\"
        page = path+directory
        for file in os.listdir(page):
            with open(page+file,'r',encoding = "utf-8") as f:
                content= f.read()
                soup = BeautifulSoup(content,'lxml')
                if soup.find('h1',class_='DDPage__header-title') != None:
                    placeName.append(soup.find_all('h1',class_='DDPage__header-title')[0].text)
                else: placeName.append("None")
                if soup.find('div',class_='item-tags col-xs-12') != None:
                    placeTags.append([soup.find_all('div',class_='item-tags col-xs-12')[0].text.replace("\n"," ")])
                else: placeTags.append("None")
                if soup.find('div',class_='title-md item-action-count') != None:
                    numPeopleVisited.append(soup.find_all('div',class_='title-md item-action-count')[0].text)
                else: numPeopleVisited.append("None")
                if soup.find('div',class_='title-md item-action-count') != None:
                    numPeopleWant.append(soup.find_all('div',class_='title-md item-action-count')[1].text)
                else: numPeopleWant.append("None")
                if soup.find('div',class_='DDP__body-copy') != None:
                    placeDesc.append(soup.find_all('div',class_='DDP__body-copy')[0].text.replace('\n',' ').replace("\xa0"," ").replace("-"," ").replace("–"," ").replace("—"," "))
                else: placeDesc.append("None")
                if soup.find('h3',class_='DDPage__header-dek') != None:
                    placeShortDesc.append(soup.find_all('h3',class_='DDPage__header-dek')[0].text.replace('\xa0',' '))
                else: placeShortDesc.append("None")
                if soup.find('div',class_='DDPageSiderailRecirc') != None:
                    placeNearby.append(list(set([soup.find_all('div',class_='DDPageSiderailRecirc')[0].text.replace("\n"," ")])))
                else: placeNearby.append("None")
                if soup.find('address',class_='DDPageSiderail__address') != None:
                    placeAddress.append(addr(soup))
                else: placeAddress.append("None")
                if soup.find('div',class_='DDPageSiderail__coordinates js-copy-coordinates') != None:
                    placeAlt.append(alt(soup))
                else: placeAlt.append("None")
                if soup.find('div',class_='DDPageSiderail__coordinates js-copy-coordinates') != None:
                    placeLong.append(long(soup))
                else: placeLong.append("None")
                if soup.find('div',class_='DDPContributorsList') != None:
                    placeEditors.append(soup.find_all('div',class_='DDPContributorsList')[0].text.replace('\n',' '))
                else: placeEditors.append("None")
                if soup.find('div',class_='DDPContributor__name') != None:
                    placePubDate.append(soup.find_all('div',class_='DDPContributor__name')[0].text.replace('\n',' '))
                else: placePubDate.append("None")
                placeUrl.append("https://www.atlasobscura.com/places/"+str(file).replace(" ","-").replace(".html", ""))
            k += 1
    df = pd.DataFrame({"placeName":placeName, "placeTags":placeTags, "numPeopleVisited":numPeopleVisited, "numPeopleWant":numPeopleWant, "placeDesc":placeDesc, "placeShortDesc":placeShortDesc, "placeNearby":placeNearby, "placeAddress":placeAddress, "placeAlt":placeAlt, "placeLong":placeLong, "placeEditors":placeEditors, "placePubDate":placePubDate, "placeUrl":placeUrl })
    
    return df.to_csv('AO_Data.csv')



#2.1

def TextPre(text):
    punctuation = string.punctuation+'’'+"“"+"”"+"–"+"—"
    stop_words = set(stopwords.words('english'))
    lemmat = WordNetLemmatizer()
    noPun = "".join([i for i in text if i not in punctuation])
    tokens = word_tokenize(noPun)
    tokens = [i.lower() for i in tokens]
    noStop = [i for i in tokens if i not in stop_words]    

    return [lemmat.lemmatize(lemmat.lemmatize(lemmat.lemmatize(i), pos="v"), pos = "a") for i in noStop]



#2.2

def NVD(txt, txtid, tfidf, dictio):
    words = set(txt)
    V = np.zeros(len(dictio))
    for word in words:
        dim = dictio[word]-1
        val = tfidf[str(dictio[word]), txtid]
        V[dim] = val
    D = V/np.linalg.norm(V)
    
    return(D)


def NVQ(txt, dictio):
    words = set(txt)
    V = np.zeros(len(dictio))
    for word in words:
        dim = dictio[word]-1
        V[dim] = 1
    if np.linalg.norm(V) != 0:
        Q = V/np.linalg.norm(V)
    else: Q = V

    return(Q)



#3

def AddPre(text):
    punctuation = string.punctuation+'’'+"“"+"”"+"–"+"—"
    stop_words = set(stopwords.words('english'))
    lemmat = WordNetLemmatizer()
    noPun = "".join([i for i in text if i not in punctuation])
    noNum = " ".join(s for s in noPun.split() if not any(c.isdigit() for c in s))
    tokens = word_tokenize(noNum)
    tokens = [i.lower() for i in tokens]
    noStop = [i for i in tokens if i not in stop_words]  
    return noStop


def NVD_add(txt, txtid, tfidf, dictio):
    words = set(txt)
    V = np.zeros(len(dictio))
    for word in words:
        dim = dictio[word]-1
        val = tfidf[str(dictio[word]), txtid]
        V[dim] = val
    if np.linalg.norm(V) != 0:
        D = V/np.linalg.norm(V)
    else: D = V
    
    return(D)


