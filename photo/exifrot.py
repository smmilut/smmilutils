"""
    Exifrot - smmilutils.photo.exifrot
    Photo rotator - rotates according to Exif orientation
    MAIN script
    
    started 2011-07-20
    by Pil Smmilut
    
"""
import sys
import getopt
import logging
import os.path
import shutil
import datetime

import smmilutils.exif.exif, smmilutils.exif.errors
import smmilutils.sysutils.fileutils, smmilutils.sysutils.errors

#==============================================================================
global logger
logger = logging.getLogger("exifrot")

#------------------------------------------------------------------------------
def init_logging(dest=None):
    """  Initialize logging defaults.  """
    # Format for the log filename
    fname_fmt = '%Y-%m-%d_%Hh%Mm%Ss_exifrot.log'
    global logger
    logger.setLevel(logging.DEBUG)
    if dest is None:
        ## Destination directory not provided for the log file
        ## Set up logging to console
        # Console log handler
        c_hand = logging.StreamHandler()
        c_hand.setLevel(logging.WARNING)
        c_fmt = logging.Formatter(
                '%(levelname)-7s - %(module)-12s: %(message)s')
        c_hand.setFormatter(c_fmt)
        logger.addHandler(c_hand)
        logger.info("Logging to console")
    else:
        ## Set logging to file
        # Destination file
        fname = os.path.join(dest, datetime.datetime.now().strftime(fname_fmt))
        # File log handler
        hand = logging.FileHandler(fname)
        hand.setLevel(logging.INFO)
        fmt = logging.Formatter(
                '%(asctime)s %(levelname)-7s - %(module)-12s: %(message)s')
        hand.setFormatter(fmt)
        logger.addHandler(hand)
        logger.info('Now also logging to file {}'.format(fname))
    
#------------------------------------------------------------------------------
def newname(fullpath,
        newfname_fmt='%Y-%m-%d_%Hh%Mm%Ss_{fname}',
        overwrite=False,
        destpath=None):
    """  Return a new name for photo from Exif metadata  """
    ## Split file name
    fpath, fname = os.path.split(fullpath)
    fname, fext = os.path.splitext(fname)
    ## Generate new name
    # Get photo date from exif data (for file naming)
    exifdate = smmilutils.exif.exif.get_exif_date(fullpath)
    # Include date in the format
    newfname_fmt = exifdate.strftime(newfname_fmt)
    # Include old filename in the format
    newname = newfname_fmt.format(fname=fname)
    if destpath is None:
        ## No outside destination
        # Don't move new file to another location
        destpath = fpath
    # Construct filename
    fullnewname = os.path.join(destpath, newname + fext)
    if os.path.isfile(fullnewname) and not overwrite:
        ## Filename already exists and we don't want to overwrite
        # We must generate a new name
        logger.warning("Destination file {} already exists.".format(
                        fullnewname))
        n = 0
        while os.path.isfile(fullnewname):
            ## Generate a new name, appending a number
            n += 1
            # Format "_001"
            appendix = "_{:03}".format(n)
            fullnewname = os.path.join(destpath,
                                        ''.join((newname, appendix, fext)))
            if n >= 999:
                ## We're going to loop forever!
                # (yeah i know the exception is not defined (yet) ! :p
                raise errors.FileAlreadyExistsError(fullnewname)
    logger.debug("{} has new name -> {}".format(fullpath, fullnewname))
    return fullnewname
#------------------------------------------------------------------------------
def straighten(fullpath,
        newfname_fmt='%Y-%m-%d_%Hh%Mm%Ss_{fname}',
        destpath=None,
        rename_anyway=False,
        overwrite=False):
    """  Rotate image in filename, to put it upside-up.

        newfname_fmt: format for the new filename ('{fname}' for no change)
        destpath: destination path or None if in place
        rename_anyway: rename even if doesn't need rotation
        overwrite: if destination file already exist, don't generate a new name
        """
    ## Get image properly rotated, and its associated exif data
    newimg, newexif = smmilutils.exif.exif.get_exif_oriented(fullpath)
    if destpath is None:
        ## No destination provided
        # put in the same location as the original
        destpath = os.path.split(fullpath)[0]
    ## Generate new file name
    fullnewname = newname(fullpath,
                    newfname_fmt=newfname_fmt,
                    overwrite=overwrite,
                    destpath=destpath)
    if newimg is None:
        ## Image was not rotated
        logger.info("{} : image was not rotated".format(fullpath))
        if rename_anyway:
            ## Just rename the image
            shutil.copy(fullpath, fullnewname)
            # apply permissions
            shutil.copystat(fullpath, fullnewname)
            logger.info("{} : renamed into -> {}".format(fullpath, fullnewname))
            return fullnewname
        ## Do nothing to the image
        return None
    ## Write new image file
    newimg.save(fullnewname)
    # apply permissions
    shutil.copystat(fullpath, fullnewname)
    logger.debug("{0} : created from {1}".format(fullnewname, fullpath))
    ## Write correct exif data to new image
    smmilutils.exif.exif.apply_new_exif(fullnewname, newexif)
    logger.debug("{} : exif data applied".format(fullnewname))
    logger.info("{0} : transformed into -> {1}".format(fullpath, fullnewname))
    return fullnewname

#------------------------------------------------------------------------------
def straighten_all(photolist,
        newfname_fmt='%Y-%m-%d_%Hh%Mm%Ss_{fname}',
        destpath=None,
        rename_anyway=True,
        overwrite=False):
    """  Straighten (rotate) all photos in the list.  """
    ## Prepare a string for indicating progression ('023/265')
    total_num = len(photolist)
    progress_str = '{{n:0{length}}}/{total}'.format(
                    length=len(str(total_num)),
                    total=total_num)
    for n, fullpath in enumerate(photolist):
        # log progression
        logger.info(''.join((progress_str.format(n=n+1), " - processing image...")))
        try:
            straighten(fullpath,
                        newfname_fmt=newfname_fmt,
                        destpath=destpath,
                        rename_anyway=rename_anyway,
                        overwrite=overwrite)
        except (smmilutils.exif.errors.PIL_OpenError,
                smmilutils.exif.errors.NoExifTagError,
                smmilutils.exif.errors.BadExifTagError,
                smmilutils.exif.errors.ExifError) as err:
            # Do not rotate, proceed to next file
            logger.warning("{0} : ERROR, file not processed : {1}".format(
                            fullpath, err))
            continue

#------------------------------------------------------------------------------
def usage():
    print """ exifrot : rotate and rename photos according to exif metadata
        Options :
    -h, --help: this message
    -o, --output: destination directory
    -f, --fmt: destination file format (like '%Y-%m-%d_%Hh%Mm%Ss_{fname}{fext}')
    -a, --rename_anyway: rename files even if not rotated
    -w, --overwrite: overwrite existing filename
    """
#==============================================================================
def main(argv):
    """  Main rotate script.  """
    # init console logging
    init_logging()
    try:
        ## Get command line options
        opts, args = getopt.getopt(argv, 'ho:f:aw',
                    ['help', 'output=', 'fmt=', 'rename_anyway', 'overwrite'])
    except getopt.GetoptError:
        logger.error("Wrong command line arguments")
        sys.exit(1)
    ## Default for options
    # destination directory
    destdir = None
    # format of new filenames
    newfname_fmt = '%Y-%m-%d_%Hh%Mm%Ss_{fname}'
    # rename even if image was not transformed
    rename_anyway = False
    # overwrite if renamed file already exist
    overwrite = False
    for opt, arg in opts:
        ## Parse command line options
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-o', '--output'):
            destdir = arg
        elif opt in ('-f', '--fmt'):
            newfname_fmt = arg
        elif opt in ('-a', '--rename_anyway'):
            rename_anyway = True
        elif opt in ('-w', '--overwrite'):
            overwrite = True
    # Work on all files given on command line
    filelist = [a for a in args if os.path.isfile(a)]
    logdest = destdir
    if logdest is None:
        ## No destination was given for log file
        # We log in the same location as the first photo to work on
        logdest = os.path.split(filelist[0])[0]
    # init logging to a file
    init_logging(logdest)
    logger.info("""options:
    destination directory: {0}
    output file format: {1}
    rename_anyway: {2}
    overwrite: {3}
    files to work on: {4}""".format(destdir,
        newfname_fmt,
        rename_anyway,
        overwrite,
        len(filelist)))
    ## Shake it
    straighten_all(filelist, newfname_fmt=newfname_fmt, destpath=destdir, rename_anyway=rename_anyway, overwrite=overwrite)
    
#------------------------------------------------------------------------------
if __name__ == "__main__":
    ## Executed as a main script
    main(sys.argv[1:])

