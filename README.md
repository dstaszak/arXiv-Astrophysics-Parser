# VHE-HE-Astrophysics-Mailing-List

VHE/HE arxiv.org parser and mailing list code

## Synopsis

Program parses the new astrophysics papers of the day and sends out a summary
email to the list defined below (searching for key words in the title/abstract).
This is tuned for papers of interest to VHE (Very High Energy, VHE: >100GeV) 
HE (High Energy, HE: >1GeV) gamma-ray astrophysics community but could be 
easily adapted to search for other specialties/interests.


## Installation

Code was written and runs with Python 2.7, untested in other versions. 
I set this to run as a cronjob on the local linux server and pointed the cronjob to 
execute a shell file that set the environmental variables and ran python.  
For example, put this file in your directory and point the cronjob to it:

#!/bin/tsch
source [home]/[Environmental Variables File]
cd [Directory]
python parseArchiveAndSendEmail.py

