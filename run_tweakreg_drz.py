#! /usr/bin/env python

'''
ABOUT:
This program runs tweakreg on a list of _fl? images

DEPENDS:
Python 2.5.4

AUTHOR:
D. HAMMER for STScI, 2013

HISTORY:
July 2013: Original script (v0.1).

FUTURE IMPROVEMENTS:

USE:
python run_tweakreg_flt.py
'''

__author__='D.M. HAMMER'
__version__= 0.1

import os, glob, argparse, pyfits, pdb
from pyraf import iraf
import numpy as np
from drizzlepac import tweakreg


if __name__=='__main__':
    # Parse input parameters
    parser = argparse.ArgumentParser(description='Run tweakreg on input images using custom source catalogs.')
    parser.add_argument('-im', '--images',default='*fl?.fits', type=str, help='Input image file(s). \
				 Default is all _fl? images in current directory.')
    parser.add_argument('-cf', '--catfile',default='catfile.sex', type=str, help='Input name of catfile. \
				 Default is catfile.sex.')
    parser.add_argument('-log', '--logfile',default='tweakreg.log', type=str, help='Input name of tweakreg log file. \
				 Default is tweakreg.log')
    parser.add_argument('-rim', '--refim',default='', type=str, help='Input reference image. \
                                 There is no default - must be entered.')
    parser.add_argument('-rcat', '--refcat',default='', type=str, help='Input image file(s). \
                                 There is no default - must be entered.')
    parser.add_argument('-xc', '--xcol',default=8, type=int, help='Input catalog column that corresponds to x. \
                                 Default = SExtractor XWIN column.')
    parser.add_argument('-yc', '--ycol',default=9, type=int, help='Input catalog column that corresponds to y. \
                                 Default = SExtractor YWIN column.')
    parser.add_argument('-rxc', '--refxcol',default=8, type=int, help='Input (ref)catalog column that corresponds to x. \
                                 Default = SExtractor XWIN column.')
    parser.add_argument('-ryc', '--refycol',default=9, type=int, help='Input (ref)catalog column that corresponds to y. \
                                 Default = SExtractor YWIN column.')
    options = parser.parse_args()
    logfile = options.logfile
    catfilename = options.catfile
    xcol = options.xcol
    ycol = options.ycol
    rxcol = options.refxcol
    rycol = options.refycol

    # -- parse input to hold image and reference info
    im = glob.glob(options.images)
    im.sort()
    irefim = glob.glob(options.refim)
    irefim.sort()
    irefcat = glob.glob(options.refcat)
    irefcat.sort()


    if len(irefim) > 0:
        irefim = irefim[0]
        irefcat = irefcat[0]
	USE_REF = True
    else:
        irefim = ''
        irefcat = ''
        USE_REF = False


    # print image list to file
    f = open('imlist.dat', 'w')
    for ff in im: f.write(ff+'\n')
    f.close()


    # -- set conv width based on filter name (IR = 2.5; optical=3.5)
    fheader = pyfits.getheader(im[0])
    instr = fheader['INSTRUME']
    if instr == 'WFC3':
        filtname = fheader['FILTER']
    else: #assuming ACS
        filtname = fheader['FILTER1']
        if filtname[0] == 'C': filtname = fheader['FILTER2']  

    if filtname[0:2] == 'F1': conv_wid = 2.5
    else: conv_wid = 3.5


    # -- run tweakreg (SExtractor catalog: XWIN cols 8/9; XORG cols 2/3)
    iraf.unlearn('tweakreg')
    if USE_REF:
        tweakreg.TweakReg('@imlist.dat',catfile=catfilename,xcol=xcol,ycol=ycol,refimage=irefim,refcat=irefcat,refxyunits='pixels',refxcol=rxcol,refycol=rycol, runfile=logfile, \
			conv_width=conv_wid,searchrad=3.0,updatehdr=True,nclip=7,shiftfile=True,outshifts='shift.dat', see2dplot=False,residplot='No plot')
    else:
        tweakreg.TweakReg('@imlist.dat',catfile=catfilename,xcol=xcol,ycol=ycol,conv_width=conv_wid,searchrad=3.0, runfile=logfile, \
			updatehdr=True,nclip=7,shiftfile=True,outshifts='shift.dat',see2dplot=False,residplot='No plot')


    # -- remove unwanted tweakreg files
    tmp=np.concatenate((glob.glob('*.coo'),glob.glob('*catalog.match'),glob.glob('shift*.fits')))
    for ff in tmp: os.remove(ff)

