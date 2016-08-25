# VHE-HE-Astrophysics-Mailing-List

Code to find new, interesting astrophysics papers posted in the last day to arXiv.org and send a formated, summary email to a mailing list.  Currently targets high energy gamma-ray astronomy topics but this can be easily retuned.

## Synopsis

Program parses the new astrophysics papers of the day and sends out a summary
email to a mailing list. 
The titles and abstracts in the papers are parsed from html and the program
searches for key words in the title/abstract.
The keywords chosen here are tuned for papers of interest to the VHE (Very High Energy, VHE: >100GeV) 
and HE (High Energy, HE: >1GeV) gamma-ray astrophysics community.
This could be easily adapted to search for other specialties/interests by 
substituting different word combinations.


## Installation

Code was written and runs with Python 2.6-2.7, untested in other versions. 
This can be run as simply as 'python parseArchiveAndSendEmail.py', however
I suggest setting it run as a cronjob on your local machine.
Note that you'll need to fill in listOfEmails = [] with valid addresses.

## Output 

Email will show up with a timestamped subject line.

      VHE/HE Papers for 2016-08-27

Email contents are formatted to fit within the default width in most modern email clients (this is a shameless plug!):

    ----- 20 Papers Related to VHE/HE Gamma-Ray Science 2015-08-27 -----

    ...

    http://arxiv.org/abs/1508.06597
    * Title:  A Cosmic-ray Electron Spectrum with VERITAS
    * Authors: David Staszak, VERITAS Collaboration
    * Comments: 7 pages, 3 figures; To appear in the Proceedings of the 34th
        International Cosmic Ray Conference (ICRC2015), The Hague, The
        Netherlands
    * Abstract:
        "Cosmic-ray electrons and positrons (CREs) at GeV-TeV energies are
        a unique probe of our local Galactic neighbourhood. CREs lose
        energy rapidly via inverse Compton scattering and synchrotron
        processes while propagating in the Galaxy, effectively placing a
        maximal propagation distance for TeV electrons of order ~1 kpc.
        Within this window, detected ..."

     --------

     http://arxiv.org/abs/1508.06622
     * Title:  Prospects On Testing Lorentz Invariance Violation With The
        Cherenkov  Telescope Array
     * Authors: M. K. Daniel, D. Emmanoulopoulos, M. Fairbairn, N. Otte, CTA
        Consortium
     * Comments: 8 pages, in Proceedings of the 34th International Cosmic Ray
        Conference (ICRC2015), The Hague, The Netherlands. All CTA
        contributions at
     * Abstract:
        "The assumption of Lorentz invariance is one of the founding
        principles of modern physics and violation of that would have deep
        consequences to our understanding of the universe. Potential
        signatures of such a violation could range from energy dependent
        dispersion introduced into a light curve to a change in the ..."

     --------

     ...