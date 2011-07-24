"""
    Exifren - smmilutils.photo.exifren
    Photo renamer - renames according to Exif date
    MAIN script
    
    started 2011-01-05
    by Pil Smmilut
    
"""
import logging
import os.path

import smmilutils.exif.exif, smmilutils.exif.errors
import smmilutils.sysutils.fileutils, smmilutils.sysutils.errors
import smmilutils.simplegui.fileselect
global FilelistGUI
FilelistGUI = smmilutils.simplegui.fileselect.getgui()

#==============================================================================
global logger

#------------------------------------------------------------------------------
def init_logging():
    """  Initialize logging defaults.  """
    ## Set up logging to console
    # Only INFO and above (not DEBUG), and replace file each time.
    logging.basicConfig(level=logging.INFO,  # level=logging.WARNING,
                        format='%(levelname)-8s - %(module)-12s: %(message)s')
    ## Init logger for this module
    global logger
    logger = logging.getLogger("exifren")
    
#------------------------------------------------------------------------------
def rename_all(photolist,
                keeporig=False,
                stoprecurse=True):
    """  Rename all photos in the list.  """
    for fullpath in photolist:
        ## Split file name
        fpath, fname = os.path.split(fullpath)
        fname, fext = os.path.splitext(fname)
        ## Get date string
        try:
            exif_date = smmilutils.exif.exif.get_exif_date(fullpath)
        except smmilutils.exif.errors.PIL_OpenError as err:
            ## PIL couldn't open the image
            # Do not rename, proceed to next file
            logger.warning("File \"%s\" not renamed." % err.filename)
            continue
        except smmilutils.exif.errors.NoExifTagError as err:
            ## Image doesn't have the exif tag
            # Do not rename, proceed to next file
            logger.warning("File \"%s\" not renamed." % err.filename)
            continue
        except smmilutils.exif.errors.ExifError:
            ## Unknown error with Exif metadata
            # Do not rename, proceed to next file
            logger.warning("File \"%s\" not renamed." % fullpath)
            continue
        # Format date string
        formatteddate = exif_date.strftime("%Y-%m-%d_%Hh%Mm%Ss")
        if stoprecurse:
            ## Stop renaming the file if it already has the proper format
            if fname.startswith(formatteddate):
                ## File already has proper format
                # Do not rename, proceed to next file
                logger.info("File \"%s\" already starts with its date." % fname)
                logger.warning("File \"%s\" not renamed." % fname)
                continue
        ## Construct new file name
        # Keep original filename inside?
        if keeporig:
            origname = "".join(("(", fname, ")"))
        else:
            origname = ""
        newname = "".join((formatteddate, origname, fext))
        ## Rename
        try:
            smmilutils.sysutils.fileutils.rename(fullpath, newname)
        except smmilutils.sysutils.errors.FileDoesntExistError:
            ## Original file doesn't exist?
            # Weird, but ok, we can't do anything
            logger.warning("File \"%s\" not renamed." % err.filename)
            continue
    

#==============================================================================
def main():
    """  Main rename script.  """
    # Default directory
    directory = "~"
    init_logging()
    logger.info("Start directory : %s" % directory)
    gui = FilelistGUI(title="Select photos to rename. (Ctrl for multiple)")
    ## Ask the user for a list of files
    filelist = gui.run()
    if not filelist:
        ## User didn't select files
        logger.info("User selected no files.")
        ## We quit
        return
    ## User selected some files
    logger.info("%i files to rename." % len(filelist))
    # Rename the shit our of them
    rename_all(filelist, keeporig=True)
    
#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
    
