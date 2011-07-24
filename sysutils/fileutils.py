"""
    smmilutils.sysutils.fileutils
    utilities for manipulating files
    
    Pil Smmilut 2011-02-12
    
"""
import os
import logging
import errors

#==============================================================================
global logger
logger = logging.getLogger("fileutils")

#------------------------------------------------------------------------------
def rename(fulloldname, newname, overwrite=False):
    """  Renames (and/or move) a file
        (FULL path of files !!)
    """
    global logger
    destpath = os.path.split(fulloldname)[0]
    fullnewname = os.path.join(destpath, newname)
    ## Check if files exist
    if not os.path.isfile(fulloldname):
        ## The file doesn't exist! Can't rename!
        logger.error("File \"%s\" doesn't exist !" % fulloldname)
        raise errors.FileDoesntExistError(fulloldname)
    if os.path.isfile(fullnewname) and not overwrite:
        ## Filename already exists and we don't want to overwrite
        # We must generate a new name
        #raise errors.FileAlreadyExistsError(fullnewname)
        logger.warning("Destination file \"%s\" already exists." % newname)
        fbase, fext = os.path.splitext(newname)
        n = 0
        while os.path.isfile(fullnewname):
            n += 1
            # Format "_001"
            appendix = "_%03.f" % n
            newnew = "".join((fbase, appendix, fext))
            fullnewname = os.path.join(destpath, newnew)
            if n >= 999:
                ## We're going to loop forever!
                raise errors.FileAlreadyExistsError(fullnewname)
    ## Rename the file !
    os.rename(fulloldname, fullnewname)
    logger.info("File \"%s\" renamed to -> \"%s\"." % (fulloldname, fullnewname))
    
#==============================================================================
if __name__ == "__main__":
    pass  # rename("caca", "cucu")
    
