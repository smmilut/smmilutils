"""
    Get a list of files using Tkinter
    
    started 2011-01-16
    by Pil Smmilut
    
"""
# For handling paths
import logging
import os.path
import tkFileDialog

#==============================================================================
global logger
logger = logging.getLogger("tkfilesel")

#------------------------------------------------------------------------------
class FilelistGUI(object):
    """  A simple GUI for asking files from a user, using Tkinter.  """
    ## File types for the file selections
    FILETYPES = [("All images", "*.JPG" ),
                 ("Image jpeg", "*.JPG" ),
                 ("All images", "*.jpg" ),
                 ("Image jpeg", "*.jpg" ),
                 ("All images", "*.jpeg" ),
                 ("Image jpeg", "*.jpeg" ),
                 ("All files", "*")]
    def __init__(self, title="Select files.", initdir="~"):
        self.filelist = None
        self.title = title
        self.set_initdir(initdir)
    
    def set_initdir(self, dirname):
        """  Set the initial directory shown by tghe GUI.  """
        # Expand the home directory of the user (if "~" is in the directory name)
        self._initdir = os.path.expanduser(dirname)
        
    def run(self):
        """  Start the GUI and return the list of selected files.
            (or [] if user pressed cancel)
        """
        ## Open a Tkinter GUI
        retval = tkFileDialog.askopenfilenames(
                    title=self.title,
                    filetypes=self.FILETYPES, initialdir=self._initdir)
        ## Save the return value as the list of files
        # Return [] if user pressed cancel
        self.filelist = retval or []
        logger.info("%i files selected." % len(self.filelist))
        return retval
        
#==============================================================================
if __name__ == "__main__":
    guiproc = FilelistGUI()
    print guiproc.filelist
    guiproc.run()
    print "\"%s\"" % guiproc.filelist
    

