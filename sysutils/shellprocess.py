"""
    smmilutils.sysutils.shellprocess
        start processes in the system shell
    
    Pil Smmilut 2011-02-10
    
"""
import subprocess, shlex
#==============================================================================
def cmd_exists(cmdname):
    """  Checks if the command exists in the system shell
        (uses 'which', so only available on unixes)
    """
    args = ['which', cmdname.strip()]
    # Redirect stdin and stdout so they don't get printed in terminals
    whichproc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    ## Call 'which cmdname'
    whichproc.communicate()
    if whichproc.returncode == 0:
        ## All specified commands are found and executable
        # cmd EXISTS
        return True
    else:
        ## Can't be found by 'which', or 'which' doesn't exist
        return False
    
#------------------------------------------------------------------------------
class ShellProcess:
    """  A shell process that can be run several time.
        You can retrieve stderr and stdout separately
    """
    def __init__(self, callstring):
        self.stdout = None
        self.stderr = None
        self.returncode = None
        # Split the command into arguments
        self._cmdargs = shlex.split(callstring)
        
    def run(self):
        """  Run the process.  """
        try:
            ## Make a shell process
            proc = subprocess.Popen(self._cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        except OSError:
            ## Could not call
            print "Error calling %s" % " ".join(self._cmdargs)
            raise
        self.stdout, self.stderr = proc.communicate()
        self.returncode = proc.returncode
        return self.returncode
    
#==============================================================================
if __name__ == "__main__":
    ## little tests
    print cmd_exists("man")
    

