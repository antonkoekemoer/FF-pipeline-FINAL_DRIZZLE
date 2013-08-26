#! /usr/bin/env python

'''
ABOUT:
This script runs SExtractor on list of images (crclean in current directory is default).

DEPENDS:
Python 2.5.4

AUTHOR:
D. HAMMER for STScI, 2013

HISTORY:
Jul 2013: Original script (v0.1).
Aug 2013: Modified to run on any instrument's image (e.g., double-chip ACS/optical or single-chip WFC/IR).


FUTURE IMPROVEMENTS:

USE:
python run_sex_crclean
'''

__author__='D.M. HAMMER'
__version__= 0.1


import os, glob, argparse, pdb, pylab, pyfits
import numpy as np
from subprocess import call


if __name__=='__main__':

    # -- Parse input parameters
    #--------------------------
    parser = argparse.ArgumentParser(description='Run SExtractor on specified images.')
    parser.add_argument('-im', '--images',default='*crclean.fits', type=str, help='Input fits file(s). \
                        Default is all CR-cleaned science images in working directory.')
    parser.add_argument('-max', '--maxobj',default=100, type=int, help='Input maximum number of SExtractor detections to use for tweakreg matching (each chip). \
                        Default is 100 objects per chip.')
    options = parser.parse_args()
    imlist = glob.glob(options.images)
    imlist.sort()
    maxobj = options.maxobj


    # -- initialize variables to hold names of catalogs for each image
    tcatnamesA_global = []
    tcatnamesB_global = []


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
            if filtname[0] == 'C': filtname == fheader['FILTER2']	

	configname = filtname.lower()+'.sex.crclean.config'


	# -- determine the science extension for each image & store chip information
	sciext = []
	chipid = []
	catname = []
	tcatname = []
        hdulist = pyfits.open(im)
        for ff in xrange(len(hdulist)):
            if hdulist[ff].name == 'SCI':
                sciext.append(ff)
                fheader = pyfits.getheader(im,ext=sciext[-1])
		chipid.append(fheader.get('CCDCHIP',default=1))
		catname.append(im.split('_')[0] +'_sci'+str(len(chipid))+'.sex.all')
                tcatname.append(catname[-1].split('.all')[0])
		if len(sciext) == 1: tcatnamesA_global.append(tcatname[-1])
		elif len(sciext) == 2: tcatnamesB_global.append(tcatname[-1])
		else: raise Exception('Unexpected number of SCI extensions (>2).')
	if len(sciext) == 1: tcatnamesB_global.append('')

        # -- run SExtractor
	for ff in xrange(len(sciext)):

		# -- create SE catalogs & make corresponding ds9 region file with Kron apertures.
		call(['sex','-c',configname,im+'['+str(sciext[ff]-1)+']','-CATALOG_NAME',catname[ff]])	# NOTE - SEXtractor does not consider the zeroth extension to be the primary extension if no science data.
		call(['cat2reg',catname[ff]])

		# -- trim catalog of sources with bad flags (29 keeps 0 & 2) AND faint sources
		#     NOTES: (1) when selecting brightest galaxies in UDF: KRON FLUX(6000 cnts --> 100 obj; 13000--> 60 obj);  APER FLUX[5/3pix](3000 cnts --> 42/25 obj, 1800 --> 72/59 obj)
		#            (2) found that using brightest galaxies selected by aper as opposed to Kron gave better tweakreg residuals
		#            (3) we now select the brightest "MAXOBJ" objects by AperFlux for input to tweakreg
		id,x,y,a,b,theta,kron,xwin,ywin,ra,dec,flux,fluxerr,mag,magerr,faper1,faper2,faper1err,faper2err,flag,sclass = np.loadtxt(catname[ff],unpack=True)
		fluxmin = sorted(faper2,reverse=True)[np.min([len(faper2),maxobj])-1]
        	gd = np.where(((np.int32(flag) & 29) == 0) & (faper2 > fluxmin))[0]		# USING APER FLUX
		np.savetxt(tcatname[ff],zip(id[gd],x[gd],y[gd],a[gd],b[gd],theta[gd],kron[gd],xwin[gd],ywin[gd],ra[gd],dec[gd],flux[gd],fluxerr[gd],mag[gd],magerr[gd],faper1[gd], faper2[gd],faper1err[gd], faper2err[gd],flag[gd],sclass[gd]))

		# -- create ds9 region files for trimmed catalog
        	call(['cat2reg',tcatname[ff]])


    # -- Create "catfile" for input to tweakreg
    #----------------------------------------
    fltlist = [imlist[ff].split('crclean')[0] + 'flt.fits' for ff in xrange(len(imlist))]
    np.savetxt('catfile.sex',zip(fltlist,tcatnamesA_global,tcatnamesB_global),fmt='%s')
