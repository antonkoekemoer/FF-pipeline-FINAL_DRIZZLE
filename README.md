FF-pipeline-FINAL
=================
Latest scripts and configuration files that will be used to align and drizzle images for the Frontier Fields. The order for calling the scripts is as follows:

1. *run_make_crclean*
    * default is to create crcleans for _flts in each separate _asn file.
    * AD uses the configuration files crclean_xxx.cfg.
    * Output: xxxxxx_crclean.fits; astrodrizzle.log

2. *run_sex_crclean*
    * creates SExtractor catalogs for each crlean image using config named [filter].sex.crclean.config.
    * removes bad sources such as objects with bad flags and keeps only 100 brightest (default).
    * creates ds9 region files for full and trimmed catalog (via the "cat2reg" gawk script).
    * creates external ascii file "catfile.sex" that will be used in step 3.
    * Output: *.sex.all = full catalog; *.sex = trimmed catalog; *.reg = ds9 region file (2); catfile.sex = tweak input

    -- OR --
    
   *run_find_crclean*
    * creates ImageFind catalogs for each crlean image.
    * removes bad sources located within 50 pixels of image edge.
    * creates external ascii file "catfile.coo" that will be used in step 3.
    * Output: *.coo = trimmed ImageFind catalog; catfile.coo = tweakreg input

3. *run_tweakreg_crclean*
    * aligns _flt images using tweakreg with external catalogs (either SExtractor or ImageFind).
    * tweakreg uses configuration files named "tweakreg_filtername.cfg."
    * Output: tweakreg.log; imlist.dat = list of flt images to align; *fit.match = catalog of matched objects

4. *run_tweakreg_make_xyresids*
    * constructs tweakreg diagnostic diagrams (delta-x/y vs x/y and vectorgram) using *fit.match files.
    * Output: xxxxx_xyresids.pdf & xxxxx_xyvector.pdf

5. *run_drizzle_crclean*
    * creates drizzled images from aligned flt images using configuration files drizzle_[instr].cfg.
    * Output: drizzled sci, wht, and ctx images; astrodrizzle.log

6. *run_sex_drz*
    * creates SExtractor catalogs for drizzled images using config named [filter].sex.drz.config.
    * removes bad sources such as objects with bad flags and keeps only 100 brightest (default).
    * creates ds9 region files for full and trimmed catalog (via the "cat2reg" gawk script).
    * Output: *.sex.all = full catalog; *.sex = trimmed catalog; *.reg = ds9 region file (2).

7. *run_tweakreg_crclean*
    * same script used to align flt images, but called with refim and refcat to align drz-->drz.
    * Output: tweakreg.log; imlist.dat = list of flt images to align; *fit.match = catalog of matched objects



