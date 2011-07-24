"""
    Get a list of files using Zenity
    
    Pil Smmilut 2011-01-18
    
"""
import logging
import os.path
from smmilutils.sysutils import shellprocess
from smmilutils.sysutils.dirutils import TempChdir

global logger
logger = logging.getLogger("zenfilesel")

#------------------------------------------------------------------------------
ZENITY_CMD = "zenity"
if not shellprocess.cmd_exists(ZENITY_CMD):
    ## Zenity not found on the system (using 'which', a unix command :-/ )
    logger.error("Command \"%s\" not found on the system" % ZENITY_CMD)
    raise ImportError("%s not found" % ZENITY_CMD)
    
#==============================================================================
class FilelistGUI(object):
    """  A simple GUI for asking files from a user, using zenity.  """
    def __init__(self, title="Select files.", initdir="~"):
        self.filelist = None
        self.set_initdir(initdir)
        self._separator = "|"
        # Zenity command
        zenfileask = ' '.join((ZENITY_CMD,
                              '--title=%s --file-selection --multiple --separator=%s'
                              % (title, self._separator)))
        try:
            ## Get Zenity process
            self.zenproc = shellprocess.ShellProcess(zenfileask)
        except OSError:
            ## Could not start zenity (not installed?)
            logger.error("Could not start zenity! (not installed?)")
            raise
    #--------------------------------------------------------------------------
    def set_initdir(self, dirname):
        """  Set the initial directory shown by tghe GUI.  """
        # Expand the home directory of the user (if "~" is in the directory name)
        self._initdir = os.path.expanduser(dirname)
        
    #--------------------------------------------------------------------------
    def run(self):
        """  Start the GUI and return the list of selected files.
            (or [] if user pressed cancel)
        """
        ## Open a zenity GUI
        # Launch the process (ask the user, using zenity's GUI)
        with TempChdir(self._initdir):
            retcode = self.zenproc.run()
        if retcode == 0:
            ## User selected some files
            # Get standard output (string containing the filenames)
            file_sel = self.zenproc.stdout
            # Remove trailing "\n" from the last file in the returned list
            file_sel = file_sel[:-1] + file_sel[-1][:-1]
            # Make it into a list
            file_sel = file_sel.split(self._separator)
        elif retcode == 1:
            ## User pressed "cancel"
            file_sel = []
        else:
            ## Return status not clear
            # Maybe the user pressed cancel ?
            #print "zenity returned", retcode
            file_sel = []
        ## Save the return value as the list of files
        # Return [] if user pressed cancel
        self.filelist = file_sel
        logger.info("%i files selected." % len(self.filelist))
        return file_sel
        
#==============================================================================
if __name__ == "__main__":
    ## A little test
    try:
        gui = FilelistGUI(initdir='~/downloads')
    except:
        ## Didn't work
        print "Error: Could not start zenity!"
        raise
    try:
        filelist = gui.run()
    except:
        ## Didn't work
        print "Error: Could not start zenity!"
        raise
    if filelist:
        ## User selected some files
        print "\nand also : ".join(filelist)
    else:
        ## User didn't select files
        print "Comme tu veux, j'm'en branle."
    

