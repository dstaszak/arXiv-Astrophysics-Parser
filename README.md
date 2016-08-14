# VHE-HE-Astrophysics-Mailing-List

VHE/HE arxiv.org parser and mailing list code

## Synopsis

Program parses the new astrophysics papers of the day and sends out a summary
email to the list defined in the code (searching for key words in the title/abstract).
This is tuned for papers of interest to VHE (Very High Energy, VHE: >100GeV) 
and HE (High Energy, HE: >1GeV) gamma-ray astrophysics community but could be 
easily adapted to search for other specialties/interests.


## Installation

Code was written and runs with Python 2.6-2.7, untested in other versions. 
The sript, parseArchiveAndSendEmail.py, is the meat of the program.
I previously simply set it to run as a cronjob on a local linux server.

## Output 

Email will show up with a title such as:

      VHE/HE Papers for 2016-08-27

and contents formatted like so...

    ----- 20 Papers Related to VHE/HE Gamma-Ray Science 2015-08-27 -----

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