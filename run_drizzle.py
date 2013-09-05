#! /usr/bin/env python

'''
ABOUT:
This program drizzles a stack of flt images.

DEPENDS:
Python 2.5.4

AUTHOR:
D. HAMMER for STScI, 2013

HISTORY:
July 2013: Original script (v0.1).

FUTURE IMPROVEMENTS:

USE:
python run_drizzle.py
'''

__author__='D.M. HAMMER'
__version__= 0.1

import os, glob, argparse, pyfits, pdb
from pyraf import iraf
import numpy as np
from drizzlepac import astrodrizzle
from stsci.tools import teal


if __name__=='__main__':
    # Parse input parameters
    parser = argparse.ArgumentParser(description='Run tweakreg on input images using custom source catalogs.')
    parser.add_argument('-im', '--images',default='*fl?.fits', type=str, help='Input image file(s). \
				 Default is all _fl? images in current directory.')
    parser.add_argument('-pf', '--pixfrac',default=1.0, type=float, help='Input AstroDrizzle "final_pixfrac" parameter. \
    				Default is 1.0')
    parser.add_argument('-ps', '--pixscale',default=-1.0, type=float, help='Input AstroDrizzle "final_scale" parameter. \
    				Default value is assigned based on instrument default pixel size.') 
    parser.add_argument('-c', '--cores',default=4, type=int, help='Input number of processing cores used by AD. \
                                 Default is 4.')
    options = parser.parse_args()


    # -- initialize variables to hold filenames & print image list to file
    NCORES = options.cores
    pixscale = options.pixscale
    pixfrac = options.pixfrac
    imlist = glob.glob(options.images)
    imlist.sort()
    f = open('imlist.dat', 'w')
    for ff in imlist: f.write(ff+'\n')
    f.close()


    # -- get instrument and filter name
    instrum = pyfits.getheader(imlist[0])['INSTRUME']
    if instrum == 'WFC3':
            filtname = pyfits.getheader(imlist[0])['FILTER']
            if pixscale < 0: pixscale = 0.1283
    elif instrum == 'ACS':
            filtname = pyfits.getheader(imlist[0])['FILTER1']
            if filtname[0] == 'C': filtname = pyfits.getheader(imlist[0])['FILTER2']
	    if pixscale < 0: pixscale = 0.0496

    # -- run AstroDrizzle
    teal.unlearn('astrodrizzle')
    iraf.unlearn('astrodrizzle')

    # MISSING STEP HERE!!!!
    # --We need to figure out which pixfrac/pixscale to select. Run test of rms/median on [WHT] image.

    if instrum == 'WFC3':
        astrodrizzle.AstroDrizzle('@imlist.dat',output=filtname.lower(),num_cores=NCORES,final_bits='64', in_memory=True,clean=True, combine_type=imedian,preseve=False, \
    				   final_wcs=True,final_rot=0.0,final_scale=pixscale,final_pixfrac=pixfrac,final_kernel='gaussian')
    elif instrum == 'ACS':
    	astrodrizzle.AstroDrizzle('@imlist.dat',output=filtname.lower(),num_cores=NCORES,final_bits='64,32',in_memory=True,clean=True, combine_type=imedian,preserve=False,\
                                   final_wcs=True,final_rot=0.0,final_scale=pixscale,final_pixfrac=pixfrac,final_kernel='gaussian')
    else: raise Exception('Instrument '+instrum+' not covered in our case list.')


    # -- remove unwanted astrodrizzle files
    tmp=np.concatenate((glob.glob('*single*fits'),glob.glob('*mask.fits'),glob.glob('tmp*.fits'), glob.glob(*blt.fits')))
    for ff in tmp: os.remove(ff)

