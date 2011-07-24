"""
    smmilutils.sysutils.errors
    exceptions for my sysutils module
    
    Pil Smmilut 2011-02-12
    
"""

class FileAlreadyExistsError(Exception):
    """  Trying to do something to a file whose name already exists.  """
    def __init__(self, filename):
        self.filename = filename
        
    def __str__(self):
        return "File named \"%s\" already exists." % self.filename
    

class FileDoesntExistError(Exception):
    """  Trying to do something to a file whose name doesn't exist.  """
    def __init__(self, filename):
        self.filename = filename
        
    def __str__(self):
        return "File named \"%s\" does not exists." % self.filename
    

