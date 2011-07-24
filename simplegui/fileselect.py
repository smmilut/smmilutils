"""
    smmilutils.simplegui.fileselect
    Get a list of files using Zenity or Tkinter
    
    Pil Smmilut 2011-02-12
    
    Very SHITTY implementation of a wrapper. VERY.
    
"""
import logging
from smmilutils.sysutils import importutils

global logger
logger = logging.getLogger("fileselect")

#==============================================================================
global MODULEPATH
MODULEPATH = "smmilutils.simplegui"
global GUItypes
GUItypes = ["tk", "zenity"]
global CLASSNAME
CLASSNAME = "FilelistGUI"

#------------------------------------------------------------------------------
def getgui(guitype="zenity"):
    """  Return FilelistGUI from selected GUI type.
        
        So shitty it makes me cry at night
    """
    for modname in GUItypes:
        ## For each type of GUI
        # full path to module
        fullmodpath = '.'.join((MODULEPATH, modname))
        try:
            # from GUImodule import FilelistGUI
            guiobj = importutils.from_import(fullmodpath, CLASSNAME)
        except ImportError:
            ## Can't load it
            logger.debug("%s GUI was not found for %s" % (CLASSNAME, modname))
        else:
            ## Successfully loaded
            logger.debug("%s GUI was found for %s" % (CLASSNAME, modname))
            if modname == guitype:
                ## It is the one requested
                return guiobj
    ## The one requested was not found, or not successfully loaded
    logger.info("%s GUI was not found for %s" % (CLASSNAME, guitype))
    # We return the last one loaded, or some cryptic exception that will make you mad :D
    return guiobj
    
#==============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s - %(module)-12s: %(message)s')
    guiclass = getgui()
    gui = guiclass()
    gui.run()
    print gui.filelist
    
