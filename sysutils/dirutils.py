"""
    smmilutils.sysutils.dirutils
    utilities for manipulating directories
    
    Pil Smmilut 2011-02-10
    
"""
import os

class TempChdir:
    """  Context manager to change directory temporarily.  """
    def __init__(self, newdir):
        self.newdir = newdir
        
    def __enter__(self):
        self.olddir = os.getcwd()
        os.chdir(self.newdir)
        
    def __exit__(self, *args):
        os.chdir(self.olddir)
    
#------------------------------------------------------------------------------
if __name__ == "__main__":
    ## Some test
    from smmilutils.sysutils import shellprocess
    myproc = shellprocess.ShellProcess("ls")
    myproc.run()
    print myproc.stdout, "\n", myproc.stderr, "\n"
    with TempChdir('../'):
        myproc.run()
        print myproc.stdout, "\n", myproc.stderr, "\n"
    myproc.run()
    print myproc.stdout, "\n", myproc.stderr, "\n"
    
