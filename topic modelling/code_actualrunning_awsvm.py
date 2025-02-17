# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 16:10:28 2021
@author: slp70
"""
import subprocess
import shutil, os
import re
import pandas as pd
from csv import writer
import numpy as np
import string
from boxsdk import DevelopmentClient

# This area runs the R script on all files in a folder; here
# the folder is ethics_csv in my case

dir = "/home/testuser/Downloads/"
dir1 = dir + "ethics_csv"
backup_dir = dir+"proj_backup"

consumption_filepath = dir + "topicmodel_sent/"
specific_folder_dir = dir+"box_upload"


#               SPLITTING large CSV file into smaller ones
og_file = 'A1_1P5_part3.csv'
data = pd.read_csv(dir1 + "/" + og_file)
rows = data.index
k = len(rows)

print(k)        #of csv files         10 is PLACEHOLDER, REPLACE WITH NUMBER OF ROWS IN DATAFRAME
for i in range(k):
    df = data[i:(i+1)]

    curr_file_name = (og_file.rsplit('.', 1)[0]) +'_'+str(i) + ('.csv')
    fullname = dir1+'/'+curr_file_name

    if isinstance(df.iloc[0].date,str):
        date1 = (df.iloc[0].date)
    else:
        date1 = (df.iloc[0].date).astype(str)

    #date1 = (df.iloc[0].date)
    #date1 = (df.iloc[0].date).astype(str)

    #print(fullname + " " + date1)
    if (date1!='Date Not Found'):
        if (date1.isdigit()):
            if (int(date1) in range(1580,1630)):        # only if within the date range, convert to csv and add to folder
                df.to_csv(fullname, index=False)
        else:
            datestr = date1
            if (datestr and datestr.strip()):
                datenum = re.search('\d{4}', datestr)
                if (datenum != None):
                    if (int(str(datenum.group(0))) in range(1580, 1630)):  # only if within the date range, convert to csv and add to folder
                        df.to_csv(fullname, index=False)

#           CALLS R SCRIPT

for filename in os.listdir(dir1):
    if (filename.endswith(".csv")) & (filename != og_file):
        subprocess.call(['Rscript',
                         "/home/testuser/Downloads/topicmodeling1.R",
                         filename])
    else:
        continue


#               automatically enters the developer token
def run(csv_file1):
    import sys
    f1 = sys.stdin
    f = open('input.txt', 'r')  # input.txt is text file that contains the developer key
    sys.stdin = f
    box_upload(csv_file1)
    f.close()
    sys.stdin = f1


#               uploads to Box
def box_upload(csv_file):
    '''
    Notes: Create a text file named app.cfg in pycharm. Add the following info in order:
            1. Client ID
            2. Client Secret
            3. Developer Token
            On the Box API site, go to your app and change settings:
            1. read and write all files and folders to Box - should be activated
            2. Manage users and manage groups - should be activated
            3. Make API calls using as-user header - should be activated
    '''
    client = DevelopmentClient()

    root_folder = client.folder('0').get()
    child_folders = root_folder.get_items(limit=100, offset=0)

    for child in child_folders:
        if child['name'] == 'Data+ Relevant Files':
            folder = client.folder(child['id']).get()
            break

    new_file = folder.upload(csv_file)

    print(f'File {new_file.name} was uploaded to {folder.name}')


def wordsearch(keyword, n, text):
    words = text.split()
    fullwords = ""
    # iterate through all the words
    for index, word in enumerate(words):
        # check if search keyword matches
        if word == keyword:
            # fetch left side words
            left_side_words1 = words[index - n: index]
            # fetch right side words
            right_side_words1 = words[index: index + n + 1]  # put index+1 if you want to avoid keyword
            str1 = " "
            left = str1.join(left_side_words1)
            right = str1.join(right_side_words1)
            fullwords = fullwords + left + " " + right + " "
    if fullwords.isspace():
        return None
    return fullwords

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

consumptionList = ["gold", "chocolate","wool", "beer", "tobacco","silver"]
def make_text_window(ratio, csv_file1):
    df1 = pd.read_csv(dir1 + '/' + csv_file1)
    pd.set_option('display.max_colwidth', None)
    alltext = str(df1[['text']])  # getting text column values from csv

    for word in consumptionList:
        surrounding = wordsearch(str(word), 5, alltext)
        pairList = []
        if (surrounding and surrounding.strip()):
            pairList.append(str(ratio))
            moretext = surrounding
            pairList.append(moretext)
            append_list_as_row(consumption_filepath+word+"_file.csv", pairList)
        else:
            continue

        # This checks whether file is relevant against a lexicon
for filename in os.listdir(dir1):
    if (filename.endswith(".txt")) and (filename != ".txt"):
        with open(dir1 + '/' + filename, 'r') as file:
            data = file.read().replace(',', "")
            data = data.replace('"', "")

        rel_lexicon = re.compile('Christian|charity|usury|luxury|avarice|greed|vanity|pride|sloth|gluttony|simony|fraud|incest|theft|deceit|lucrum|cessans|stations|station|silk|velvet|damask|cinnamon|pepper|ginger|sumptuary|laws|abnegatio|self-denial|mendicancy|sin|root|evil|render|caesar|heresy|prodigality|prodigal||seed|soil|crop|yield|kingdom|field|sow|sowed|wheat|barn|weeds|enemy|treasure|treasures|rust|steel|heart|gold|silver|copper|belt|belts|worker|staff|journey|thorns|deceit|wealth|rich|riches|green|righteous|righteousness|thrive|leaf|leaves|wise|store|gulp|choice|food|oil|glance|sprout|sky|eagle|endure|crown|generation|secure|trust|security|fortune|sun|radiance|moon|splendor|rich|arrogant|hope in wealth|tower|pleasant|palace|deceive|tempt|free|money|content|material possession|in need|goods|brother|sister|eve|adam|samson|delilah|david|bathsheba|lust|lustful|lustfully|sin|devil|lechery|whore|cuckold|unnatural|natural|obey|disobey|deceive|cheat|cheating|modesty|sermon|christ|heaven|godly|saint|altar|candles|canon|mass|sacrament|cross|pastor|ritual|cleansing|church|salvation|savior|jesus|lord|witness|saved|communion|wine|bread|faith|anathema|anointing|apostle|apocalypse|atonement|baptism|holy|sacred|spirit|bishop|born-again|calvinist|evangelical|protestant|catholic|covenant|conviction|creed|demon|deacon|disciple|disciples|satan|satanic|fellowship|gospel|hallelujah|hell|indulgence|indulgent|justify|justification|lucifer|messiah|manifestation|god|zion|ordained|ordinance|ordinate|congregation|parish|parishioner|prophet|repent|sanctuary|redeem|redeemed|sanctified|sanctify|second|coming|testament|tribulation|trinity|words|bible|word|grace|absolution|adultery|obedience|anoint|antichrist|archangel|armageddon|ascension|atone|vision|biblical|blasphemy|bless|blessing|blessed|chalice|chapel|chaplain|cherub|condemnation|condemn|confession|confess|conscience|consecration|contrite|contrition|damnation|damned|damn|day|divine|doctrine|ecumenical|epistle|eternal|evangelicalism|excommunication|exile|resurrection|forgive|forgiveness|freedom|fundamental|gentile|revelation|heresy|Jehovah|judgment|judaism|supper|liturgy|ministry|missionary|mission|ordination|orthodox|pagan|pagans|paganism|passover|papacy|pope|christianity|abraham|penance|genesis|exodus|leviticus|numbers|deuteronomy|moses|union|pray|prayer|predestination|prophecy|psalm|psalms|providence|purgatory|rapture|reconciliation|reconcile|redemption|reform|reformed|reincarnation|reincarnate|resurrect|roman|rome|sabbath|sacrifice|sacrifices|satanism|save|saved|sinful|nature|creation|create|death|offering|offerings|tongues|soul|commandments|transgression|universal|moral|venial|virgin|perfect|vulgate|worship|scripture|scriptures|priesthood|ten|twelve|annihilate|proverb|proverbs|matthew|mark|luke|john|peter|john|james|samuel|timothy|isaiah|hebrew|hebrews|job|slave|slaves|human|reap|holiness|parable|parables|knowledge|seed|seeds|samaritan|sown|abundance|persecution|deceitful|fruitful|unfruitful|plant|planted|reject|rejected|integrity|rejoice|rejoiced|wealth|wicked|destruction|grievance|desire|desires|entice|enticed|unfaithful|tenant|tenants|guilt|guilty|splendor|curse|almighty|defile|defiled|falsehood|false|lie|lies|confront| confronts|contempt')
        phil_lexicon = re.compile('Oikonomike|chrematistike|liberality|megalopsychos|meanness|Aristotelian|aischrokerdia|state|economics|politics|polis|politike|capacity|dynamis|science|good|agathon|life|economy|habit|physics|metaphysics|mathematics|transitive|prâxis|chresasthai|chocolate|potatoes|good|pleasure|happiness|ethics|sake|morality|teleology|teleological|eudemonic|logos|pathos|virtue|vices|courage|justice|prudence|statesmanship|friendship|Socrates|Homer|Meno|Plato|school|citizen|psyche|cumin-splitters|Athens|Thebes|Syracuse|Dionysius|Corinthians|Agamemnon|aesymnetae|sceptrer|oligarchy|demagogue')
        filename_csv = (filename.rsplit('.', 1)[0]) + ('.csv')

        mainratio = 0

        # make_text_window(data, filename_csv, filename) #MOVE THIS INTO IF STATEMENT and uncomment below stuff

        if ((re.search(rel_lexicon, data) != None) and (re.search(phil_lexicon, data) != None)):
            rel_ratio = len(re.findall(rel_lexicon, data)) / 20.0
            phil_ratio = len(re.findall(phil_lexicon, data)) / 20.0
            mainratio = phil_ratio / rel_ratio

            df = pd.read_csv(dir1 + "/" + filename_csv)
            df["ratio"] = mainratio
            df.to_csv(dir1 + "/" + filename_csv, index=False)
            make_text_window(mainratio, filename_csv)

            shutil.move(dir1 + "/" + filename_csv, specific_folder_dir)
            #run(dir1 + "/" + filename_csv)  # uploading to box if relevant
        elif (re.search(rel_lexicon, data) != None):
            mainratio = 0

            df = pd.read_csv(dir1 + "/" + filename_csv)
            df["ratio"] = mainratio
            df.to_csv(dir1 + "/" + filename_csv, index=False)
            make_text_window(mainratio, filename_csv)

            shutil.move(dir1 + "/" + filename_csv, specific_folder_dir)
            #run(dir1 + "/" + filename_csv)  # uploading to box if relevant
        elif (re.search(phil_lexicon, data) != None):
            mainratio = 10000

            df = pd.read_csv(dir1 + "/" + filename_csv)
            df["ratio"] = mainratio
            df.to_csv(dir1 + "/" + filename_csv, index=False)
            make_text_window(mainratio, filename_csv)

            shutil.move(dir1 + "/" + filename_csv, specific_folder_dir)
            #run(dir1 + "/" + filename_csv)  # uploading to box if relevant
        else:
            continue
    else:
        continue

                #CLEANING UP ethics_csv for next one
for filename in os.listdir(dir1):
    if (not filename.startswith('.') and (filename.endswith(".csv") or filename.endswith(".txt"))):
        shutil.move(dir1+"/"+filename, backup_dir)
