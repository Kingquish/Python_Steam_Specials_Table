#from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller
import time
import bs4

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Html var creation
my_url = "https://store.steampowered.com/specials"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

#Raw Arrays
gameTitles = page_soup.findAll("div", {"class":"tab_item_name"})
gameSalePercent = page_soup.findAll("div", {"class":"discount_pct"})
gameSaleOriginalPrice = page_soup.findAll("div", {"class":"discount_original_price"})
gameSaleNewPrice = page_soup.findAll("div", {"class":"discount_final_price"})

#String Conversion
strTitles = str(gameTitles)
strPercent = str(gameSalePercent)
strOriginal = str(gameSaleOriginalPrice)
strNew = str(gameSaleNewPrice)

print("Enter in the highest discount price: ")
maxPrice = input()


#Percent Off
percentTemp = ""
for i in range(len(strPercent)):
    if(strPercent[i].isdigit() == True or strPercent[i] == "%"):
        percentTemp += strPercent[i]
        if(strPercent[i] == "%"):
            percentTemp += " "
strPercent = percentTemp
gameSalePercent = strPercent.split("% ")

def IsLetter(letter):
    letterArray = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(letterArray)):
        if(letter.lower() == letterArray[i]):
            return True
    return False


#Title
nameTemp = ""
doRecord = False
for i in range(len(strTitles)):

    if(strTitles[i] == "<"):
        doRecord = False
    if(strTitles[i - 1] == ">"):
        doRecord = True
    if(doRecord):
        if(IsLetter(strTitles[i]) or strTitles[i].isdigit() or strTitles[i] == " " or strTitles[i] == ","):
            nameTemp += strTitles[i]

gameTitles = nameTemp.split(", ")


#Game Original Price
originalTemp = ""
for i in range(len(strOriginal)):
    if(strOriginal[i].isdigit() == True or strOriginal[i] == "$" or strOriginal[i] == "."):
        originalTemp += strOriginal[i]
strOriginal = originalTemp
gameSaleOriginalPrice = strOriginal.split("$")
gameSaleOriginalPrice.pop(0)


#Game Discount Price
originalTemp = ""
for i in range(len(strNew)):
    if(strNew[i].isdigit() == True or strNew[i] == "$" or strNew[i] == "."):
        originalTemp += strNew[i]
strNew = originalTemp
gameSaleNewPrice = strNew.split("$")
gameSaleNewPrice.pop(0)

#tags

tagArray = page_soup.findAll("div", {"class":"tab_item_top_tags"})
doRecord = False
newTagArray = []

for i in range(len(tagArray)):
    currentTagList = str(tagArray[i])
    currentTagFilter = ""
    for j in range(len(currentTagList)):
        if (currentTagList[j] == "<"):
            doRecord = False
        if (currentTagList[j] == ">"):
            doRecord = True
        if (doRecord):
            currentTagFilter += currentTagList[j]

    currentTagFilter = currentTagFilter.replace(">", " ")
    currentTagFilter = currentTagFilter.replace(" ,", ",")
    currentTagFilter = currentTagFilter.lstrip()
    currentTagFilter = currentTagFilter.rstrip()
    newTagArray.append(currentTagFilter)


print("|GAME TITLE|\t\t\t\t\t\t\t  |PERCENTAGE|\t|OLD >>> NEW PRICE|\t\t|GAME TAGS|")
#Fix length of title and print
for i in range(len(gameTitles)):

    currentTitle = str(gameTitles[i])
    if(len(currentTitle) > 40):
        currentTitle = currentTitle[0:40]
        currentTitle += "..."

    while(len(currentTitle) < 45):
        currentTitle += " "

    if(float(gameSaleNewPrice[i]) <= float(maxPrice)):
        print(currentTitle + "(" + gameSalePercent[i] + "%)\t\t $" + gameSaleOriginalPrice[i] + "\t>>>\t$" + gameSaleNewPrice[i] + "\t\t Tags: " + newTagArray[i])
        print("")





