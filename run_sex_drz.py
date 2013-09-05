#! /usr/bin/env python

'''
ABOUT:
This script runs SExtractor on a list of drizzled images (no default - must input filenames).

DEPENDS:
Python 2.5.4

AUTHOR:
D. HAMMER for STScI, 2013

HISTORY:
Jul 2013: Original script (v0.1).
Aug 2013: Modified to run on any instrument's image (e.g., double-chip ACS/optical or single-chip WFC/IR).


FUTURE IMPROVEMENTS:

USE:
python run_sex_drz.py
'''

__author__='D.M. HAMMER'
__version__= 0.2


import os, glob, argparse, pdb, pylab, pyfits
import numpy as np
from subprocess import call


if __name__=='__main__':

    # -- Parse input parameters
    #--------------------------
    parser = argparse.ArgumentParser(description='Run SExtractor on specified images.')
    parser.add_argument('-im', '--images',default='', type=str, help='Input fits file(s). \
                        No default selected - must input image(s).')
    parser.add_argument('-max', '--maxobj',default=100, type=int, help='Input maximum number of SExtractor detections to use for tweakreg matching (each chip). \
                        Default is 100 objects per chip.')
    options = parser.parse_args()
    imlist = glob.glob(options.images)
    imlist.sort()
    maxobj = options.maxobj


    # -- Run SExtractor on each image
    #--------------------------------
    for im in imlist:

	# -- get filter name
        fheader = pyfits.getheader(im)
        instr = fheader['INSTRUME']
        if instr == 'WFC3':
            filtname = fheader['FILTER']
        else: #assuming ACS
            filtname = fheader['FILTER1']
            if filtname[0] == 'C': filtname = fheader['FILTER2']	


	# -- get config name
	configname = filtname.lower()+'.sex.drz.config'

	# -- assign output catalog name
	catname = im.split('fits')[0]+'sex.all'
	tcatname = im.split('fits')[0]+'sex'

        # -- run SExtractor
	call(['sex','-c',configname,im,'-CATALOG_NAME',catname])
	call(['cat2reg',catname])

	# -- trim catalog of sources with bad flags (29 keeps 0 & 2) AND faint sources
	id,x,y,a,b,theta,kron,xwin,ywin,ra,dec,flux,fluxerr,mag,magerr,faper1,faper2,faper1err,faper2err,flag,sclass = np.loadtxt(catname,unpack=True)
	fluxmin = sorted(faper2,reverse=True)[np.min([len(faper2),maxobj])-1]
       	gd = np.where(((np.int32(flag) & 29) == 0) & (faper2 > fluxmin))[0]		# USING APER FLUX
	np.savetxt(tcatname,zip(id[gd],x[gd],y[gd],a[gd],b[gd],theta[gd],kron[gd],xwin[gd],ywin[gd],ra[gd],dec[gd],flux[gd],fluxerr[gd],mag[gd],magerr[gd],faper1[gd], faper2[gd],faper1err[gd], faper2err[gd],flag[gd],sclass[gd]))

	# -- create ds9 region files for trimmed catalog
       	call(['cat2reg',tcatname])
