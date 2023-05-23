import scrapy
import os
import re
import string
import subprocess
import time 



#os.chdir(r"/Users/isaacng/Library/CloudStorage/OneDrive-ImperialCollegeLondon/ME4/FYP/Search-Widget-FYP/Documentation_scraper")

appDir = '/Users/isaacng/Developer/FYP'

cwd = os.getcwd()
print("Current Directory = " + cwd)

os.system('cd ' + appDir)

spidersList = os.popen('scrapy list').read()
spidersList = spidersList.split('\n')
spidersList.remove('')

spider = input ("Type the name of the spider you would like to spider or all: \n")


if spider == "all" :
    os.system('cd /Users/isaacng/Developer/FYP')
    for i in range (len(spidersList)):
        os.system('rm ' + spidersList[i] + '_scrapped_items.csv')
        os.system('cd '+ cwd)
        os.system('scrapy crawl '+ spidersList[i] +' -o ' + spidersList[i] + '_scrapped_items.csv')

else:
    spider = spider + "_spider"
    os.system('cd /Users/isaacng/Library/CloudStorage/OneDrive-ImperialCollegeLondon/ME4/FYP/Search-Widget-FYP/Documentation_scraper')
    os.system('rm ' + spider + '_scrapped_items.csv')
    os.system('cd /Users/isaacng/Library/CloudStorage/OneDrive-ImperialCollegeLondon/ME4/FYP/Search-Widget-FYP/Documentation_scraper')
    os.system('scrapy crawl '+ spider +' -o ' + spider + '_scrapped_items.csv')
