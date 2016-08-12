#!/usr/bin/python

# Program parses the new astrophysics papers of the day and sends out a summary
# email to the list defined below (searching for key words in the title/abstract)
# Program is tuned for papers of interest to VHE (Very High Energy, VHE: >100GeV) 
# HE (High Energy, HE: >1GeV) gamma-ray astrophysics.
#
# D.Staszak, McGill University, May, 2014

import os
import sys, urllib, urllib2
import lxml.etree
from time import strftime
from datetime import timedelta
import textwrap
import itertools

print "Running for date:",strftime("%Y-%m-%d"),"or...",strftime("%a, %d %b")
dateStr = strftime("%Y-%m-%d")
dateSearchStr = ""
if int(strftime("%d")) < 10: 
    dateSearchStr = "announced " + strftime("%a") + ",  " + strftime("%d").lstrip('0') + " " + strftime("%b")
else:
    dateSearchStr = "announced " + strftime("%a, %d %b")
print "HERE",dateSearchStr


fName1 = "txtFiles/vhePapers_" + dateStr + ".txt"
fName3 = "txtFiles/vhePapersFound_" + dateStr + ".txt"
f  = open(fName1,"w")
f3 = open(fName3,"w")



parser = lxml.etree.HTMLParser(encoding='utf-8')

# Read as a string if directly from the web (.read() turns it into a string)
content = urllib2.urlopen('http://arxiv.org/list/astro-ph/new').read()
tree = lxml.etree.fromstring(content, parser) # RETURNS ElementTree object

# Check if the data is there
if content.find(dateSearchStr) == -1:
    print "Date string not found"
else: 
    print "Date string found"


#<dl></dl> tags start and end the papers for a particular section...
# i.e. "New submissions for...", "Cross-lists for ...", etc
dlSearch = tree.findall(".//dl")

papersList = []

####STEP INTO CHILDREN AS OPPOSED TO LOOP!!!!####
#<dl> and <dd> are seperate items in loop... not the best way to do this...
rememberArxivNum = ""


if content.find(dateSearchStr) == -1:
    print "Date string not found"

else: 
    print "Date string found"

    for childDD in itertools.chain(dlSearch[0], dlSearch[1]): 

        thisTitle = "NONE"
        thisAbstract = "NONE"
        thisAuthor = ""
        thisComment = "NONE"
        
        #<dt></dt> is the item info (including archive number)
        if childDD.tag.find("dt") != -1:
            
            for childSpanDT in childDD:
                
                if childSpanDT.attrib.get("class") == 'list-identifier' and childSpanDT.tag == 'span':
                    
                    for childA in childSpanDT:
                        
                        if childA.attrib.get("title") == 'Abstract' and childA.tag == 'a':
                            rememberArxivNum = "http://arxiv.org/abs/" + childA.text[6:]

        #<dd></dd> tags are the start and end of a single paper info
        if childDD.tag.find("dd") != -1:  
        
            for childDivMeta in childDD:
            
                # this is the meta-data tag, below which contains all 
                # the relevant sub-info
                if childDivMeta.tag.find("div") != -1:
                
                    for childDATA in childDivMeta:

                        if childDATA.attrib.get("class") == 'list-title':
                            for childSpan in childDATA:
                                if childSpan.attrib.get("class") == 'descriptor' and childSpan.tag == 'span':
                                    thisTitle = childSpan.tail.encode('utf-8')

                        if childDATA.attrib.get("class") == 'list-comments':
                            for childSpan2 in childDATA:
                                if childSpan2.attrib.get("class") == 'descriptor' and childSpan2.tag == 'span':
                                    thisComment = childSpan2.tail.strip()

                        if childDATA.attrib.get("class") == 'list-authors':
                            for childAu in childDATA:
                                if childAu.tag == 'a' and thisAuthor == "":
                                    thisAuthor += childAu.text.encode('utf-8').strip()
                                elif childAu.tag == 'a' and thisAuthor != "":
                                    thisAuthor += ", "
                                    thisAuthor += childAu.text.encode('utf-8').strip()

                        if childDATA.tag == "p":                         
                            thisAbstractTemp = childDATA.text.encode('utf-8').strip()
                            for childAbEl in childDATA:
                                if childAbEl.tag == 'br':
                                    thisAbstractTemp += childAbEl.tail.encode('utf-8').strip()
                            thisAbstract = textwrap.dedent(thisAbstractTemp).strip()

                    thisAuthor2 = ''.join(thisAuthor)
                    # Fill it for all found papers
                    papersList.append([thisTitle, thisAbstract, thisAuthor2, thisComment, rememberArxivNum])


print "\n\nNumber of papers in list: ",len(papersList)


for paper in papersList:
    f.write(paper[4])
    f.write("\nTitle:\n")
    f.write(paper[0])
    f.write("\nAbstract:\n")
    f.write(paper[1])
    f.write("\nAuthor:\n")
    f.write(paper[2])
    f.write("\nComment:\n")
    f.write(paper[3])
    f.write("\n\n")


gotchaPapers = 0
saveFoundStr = ""

for paper in papersList:
    
    # trick to avoid wrapping lines in string search...
    searchAbstract = textwrap.fill(paper[1],width=10000)
    searchTitle = textwrap.fill(paper[0],width=10000)


    # Words to search the text for... no doubt there is a better way to do this, but it works for now!
    if ( (searchTitle.find('VERITAS') != -1) or (searchAbstract.find('VERITAS') != -1) or 
         (searchTitle.find('Veritas') != -1) or (searchAbstract.find('Veritas') != -1) or 
         (searchTitle.find('MAGIC') != -1) or (searchAbstract.find('MAGIC') != -1) or 
         (searchTitle.find('H.E.S.S.') != -1) or (searchAbstract.find('H.E.S.S.') != -1) or 
         (searchTitle.find('HESS') != -1) or (searchAbstract.find('HESS') != -1) or
         (searchTitle.find('CTA') != -1) or (searchAbstract.find('CTA') != -1) or
         (searchTitle.find('Cherenkov Telescope Array') != -1) or (searchAbstract.find('Cherenkov Telescope Array') != -1) or
         (searchTitle.find('HAWC') != -1) or (searchAbstract.find('HAWC') != -1) or
         (searchTitle.find('High Altitude Water Cherenkov') != -1) or (searchAbstract.find('High Altitude Water Cherenkov') != -1) or
         (searchTitle.find('Fermi Large Area Telescope') != -1) or (searchAbstract.find('Fermi Large Area Telescope') != -1) or
         (searchTitle.find('Fermi Gamma Ray Space Telescope') != -1) or (searchAbstract.find('Fermi Gamma Ray Space Telescope') != -1) or
         (searchTitle.find('Fermi LAT') != -1) or (searchAbstract.find('Fermi LAT') != -1) or
         (searchTitle.find('Fermi-LAT') != -1) or (searchAbstract.find('Fermi-LAT') != -1) or

         ((searchAbstract.find('Fermi') != -1) and (searchAbstract.find('Large Area Telescope') != -1)) or 
         ((searchAbstract.find('Fermi') != -1) and (searchAbstract.find('LAT') != -1)) or 
         ((searchAbstract.find('Fermi') != -1) and (searchAbstract.find('gamma-ray') != -1)) or 
         ((searchAbstract.find('Fermi') != -1) and (searchAbstract.find('gamma;-ray') != -1)) or 
         ((searchAbstract.find('Fermi') != -1) and (searchAbstract.find('gamma ray') != -1)) or 

         (searchTitle.find('Very High Energy') != -1) or (searchAbstract.find('Very High Energy') != -1) or
         (searchTitle.find('Very high energy') != -1) or (searchAbstract.find('Very high energy') != -1) or
         (searchTitle.find('very-high-energy') != -1) or (searchAbstract.find('very-high-energy') != -1) or
         (searchTitle.find('VHE') != -1) or (searchAbstract.find('VHE') != -1) or

         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('pulsar') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('supernova remnant') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('supernova remnants') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('SNRs') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('AGN') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('binary') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('binaries') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('blazar') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('TeV') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('Tev') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('Cherenkov') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('Dark Matter') != -1)) or 
         ((searchAbstract.find('$\gamma$-ray') != -1) and (searchAbstract.find('dark matter') != -1)) or 

         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('pulsar') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('supernova remnant') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('supernova remnants') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('SNRs') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('AGN') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('blazar') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('binary') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('binaries') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('TeV') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('Tev') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('Cherenkov') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('Dark Matter') != -1)) or 
         ((searchAbstract.find('gamma-ray') != -1) and (searchAbstract.find('dark matter') != -1)) or 

         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('pulsar') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('supernova remnant') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('supernova remnants') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('SNRs') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('AGN') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('blazar') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('binary') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('binaries') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('TeV') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('Tev') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('Cherenkov') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('Dark Matter') != -1)) or 
         ((searchAbstract.find('gamma;-ray') != -1) and (searchAbstract.find('dark matter') != -1)) or 

         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('pulsar') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('supernova remnant') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('supernova remnants') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('SNRs') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('AGN') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('blazar') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('binary') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('binaries') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('TeV') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('Tev') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('Cherenkov') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('Dark Matter') != -1)) or 
         ((searchAbstract.find('gamma ray') != -1) and (searchAbstract.find('dark matter') != -1))
         ):
        
        
        # false positives to avoid:
        if ( (searchTitle.find('RHESSI') != -1) or (searchAbstract.find('RHESSI') != -1) or
             (searchTitle.find('CHESS') != -1) or (searchAbstract.find('CHESS') != -1) or
            ((searchAbstract.find('soft gamma-ray') != -1) and (searchAbstract.find('Fermi') == -1)) ):
            print "forget about it..."
            
        else:  
            gotchaPapers += 1

            ##### ARXIV ADDRESS #####
            saveFoundStr += paper[4]
            saveFoundStr += "\n"

            ##### TITLE #####
            saveFoundStr += textwrap.fill("* Title: " + paper[0], initial_indent='', subsequent_indent='        ', width=75)
            saveFoundStr += "\n"

            ##### AUTHORS - limit the number...  #####
            numWordsAuthors = len(textwrap.fill(paper[1], initial_indent='', subsequent_indent='        ', width=100000).split())
            stripTempAu = textwrap.fill(paper[2], initial_indent='', subsequent_indent='', width=10000)
            stripTempAu2 = ""
            countWordAuthors = 0
            for chAu in stripTempAu:    
                if (countWordAuthors < 15):
                    if (chAu == "," and countWordAuthors == 14):
                        countWordAuthors += 1                        
                    elif (chAu == ","):
                        countWordAuthors += 1
                        stripTempAu2 += chAu
                    else: 
                        stripTempAu2 += chAu                    
            if countWordAuthors > 14:
                saveFoundStr += textwrap.fill("* Authors: " + stripTempAu2 + "...", initial_indent='', subsequent_indent='        ', width=75)
            else:
                saveFoundStr += textwrap.fill("* Authors: " + stripTempAu2, initial_indent='', subsequent_indent='        ', width=75)


            ##### COMMENTS #####
            saveFoundStr += "\n"
            saveFoundStr += textwrap.fill("* Comments: " + paper[3], initial_indent='', subsequent_indent='        ', width=75)


            ##### ABSTRACT - limit the number of words #####
            numWordsAbstract = len(textwrap.fill(paper[1], initial_indent='', subsequent_indent='        ', width=100000).split())
            stripTemp = textwrap.fill(paper[1], initial_indent='', subsequent_indent='        ', width=10000)
            stripTemp2 = ""
            countWordAbstract = 0
            for ch in stripTemp:                
                if (countWordAbstract < 50):
                    stripTemp2 += ch
                    if (ch == " "):
                        countWordAbstract += 1
            if countWordAbstract > 49:
                stripTemp3 = "\"" + stripTemp2 + "...\""
            else: 
                stripTemp3 = "\"" + stripTemp2 + "\""
            saveFoundStr += "\n* Abstract:\n"
            saveFoundStr += textwrap.fill(stripTemp3, initial_indent='        ', subsequent_indent='        ', width=75)        
            saveFoundStr += "\n\n"

            if gotchaPapers > 0:
                saveFoundStr += "--------\n\n"

print "Caught ",gotchaPapers," papers"


if gotchaPapers > 0:
    if (gotchaPapers == 1):
        f3.write("----- " + str(gotchaPapers) + " Paper Related to VHE/HE Gamma-Ray Science " + dateStr + " ----- ")
    else:
        f3.write("----- " + str(gotchaPapers) + " Papers Related to VHE/HE Gamma-Ray Science " + dateStr + " ----- ")
    f3.write("\n\n")
    f3.write(saveFoundStr)
f3.close()

# This should be in a separate file, but it isn't for now
listOfEmails = ["Name\@Email.Address"]

if gotchaPapers > 0:
    for email in listOfEmails:
        mailString = "cat " + fName3 + " | mailx -s \"VHE/HE Papers for " + dateStr + " \" " + email
        print mailString
        os.system(mailString)

    
