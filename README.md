FF-pipeline-FINAL
=================
Latest scripts and configuration files that will be used to align and drizzle images for the Frontier Fields. The order for calling the scripts is as follows:

1. *run_make_crclean*
    * _Purpose_: create crclean images for flts located in asn file (default), or any specified flts.
    * _Output_: [flt root]_crclean.fits; crclean.log (default)
    * _Options_:  
               [-a asn filename] [-log  AD log filename] [-c  AD # cores]  
               [-na switch "no asn" to use all flts in cwd] [-im  flt images to use when -na switch is on]
    * _Examples_:  
         >python run_make_crclean.py -c 10  [make crcleans separately for each asn file in cwd, using 10 cores].  
         >python run_make_crclean.py -na    [make crcleans in one call using all *fl?.fits images in cwd].

2. *run_sex_crclean*
    * _Purpose_: creates SExtractor catalogs for crclean images using config named [filter].sex.crclean.config.
    * makes trimmed catalog by keeping only the brightest objects (100 is default) with reliable flags (0 or 2).
    * creates ds9 region files for full and trimmed catalog (via the "cat2reg" gawk script).
    * creates external ascii file "catfile.sex" that will be used in step 3.
    * _Output_: *.sex.all = full catalog; *.sex = trimmed catalog; *.reg = ds9 region file (2); catfile.sex = Step 3 tweak input
    * _Options_: [-im images] [-max maximum objects to keep in trimmed catalog]
    * _WARNING_: expects default.param, default.conv, default.nnw, cat2reg files, & [filter].sex.crclean.config in cwd.

    -- OR --

   *run_find_crclean* (temporary name holder - script is being written)
    * creates ImageFind catalogs for each crlean image.
    * removes sources located within 50 pixels of image edge.
    * creates external ascii file "catfile.coo" that will be used in step 3.
    * Output: *.coo = trimmed ImageFind catalog; catfile.coo = tweakreg input

3. *run_tweakreg_flt*
    * _Purpose_: align flt images with tweakreg using external catalogs (either SExtractor,ImageFind, or hst2align).
    * _Output_: tweakreg.log; imlist.dat = list of flt images to align; *fit.match = catalog of matched objects
    * _Options_:  
               [-im images] [-cf catfile name] [-log tweakreg logfile name] [-rim ref image] [-rcat ref catalog]  
               [-xc catalog x column] [-yc catalog y column] [-rxc refcat x column] [-ryc refcat y column]

4. *run_tweakreg_make_xyresids*
    * _Purpose_: constructs tweakreg diagnostic diagrams (delta-x/y vs x/y and vectorgram) using *fit.match files.
    * _Output_: xxx_xyresids.pdf & xxx_xyvector.pdf
    * _Options_: [-cat tweakreg *fit.match catalogs]
    * _WARNING_: expects corresponding flt files in same directory.

5. *run_drizzle*
    * _Purpose_: creates drizzled images from a stack of aligned flt images.
    * _Output_: drizzled sci, wht, and ctx images; astrodrizzle.log (default); "imlist.dat" - list of images to drizzle
    * _Options_: [-im images] [-pf AD final_pixfrac value] [-ps AD final_scale value] [-c # cores]

6. *run_sex_drz*
    * _Purpose_: creates SExtractor catalogs for drizzled images using config named [filter].sex.drz.config.
    * makes trimmed catalog same as step2 above (i.e., select on flags & flux), but also selects stars using CLASS_STAR parameter.
    * creates ds9 region files for full and trimmed catalog (via the "cat2reg" gawk script).
    * _Output_: *.sex.all = full catalog; *.sex = trimmed catalog; *.reg = ds9 region file (2); catfile.sex = Step 7 tweakreg catfile
    * _Options_: [-im images] [-max maximum objects to keep in trimmed catalog]
    * _WARNING_: expects default.param, default.conv, default.nnw, cat2reg files, & [filter].sex.drz.config in cwd.

7. *run_tweakreg_drz*
    * _Purpose_: same script used to align flt images, but called with refim and refcat to align drz-->drz.
    * _Output_: tweakreg.log; imlist.dat = list of flt images to align; *fit.match = catalog of matched objects
    * _Options_:  
               [-im images] [-cf catfile name] [-log tweakreg logfile name] [-rim ref image] [-rcat ref catalog]  
               [-xc catalog x column] [-yc catalog y column] [-rxc refcat x column] [-ryc refcat y column]

8. *run_tweakreg_make_xyresids*  (SAME AS STEP4 BUT MAKES DIAGRAMS FOR DRZ-->DRZ DIAGRAMS -- UNDER CONSTRUCTION)
    * _Purpose_: constructs tweakreg diagnostic diagrams (delta-x/y vs x/y and vectorgram) using *fit.match files.
    * _Output_: xxx_xyresids.pdf & xxx_xyvector.pdf
    * _Options_: [-cat tweakreg *fit.match catalogs]
    * _WARNING_: expects corresponding drz files in same directory.
