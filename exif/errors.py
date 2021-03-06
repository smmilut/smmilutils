"""
    Exif exceptions
    
    started 2011-01-05
    by Pil Smmilut
    
"""

class PIL_OpenError(Exception):
    """  PIL couldn't open the file.  """
    def __init__(self, filename):
        self.filename = filename
        
    def __str__(self):
        return "File \"%s\" could not be opened by PIL." % self.filename
    

class NoExifTagError(Exception):
    """  Exif metadata doesn't contain said tag.  """
    def __init__(self, tagname, filename=""):
        self.tagname = tagname
        self.filename = filename
        
    def __str__(self):
        return "Exif: tag \"%s\" not found in file" % self.tagname
    
class BadExifTagError(Exception):
    """  Exif metadata is wrong somehow.  """
    def __init__(self, tagname, filename=""):
        self.tagname = tagname
        self.filename = filename
        
    def __str__(self):
        return "Exif: tag {0} is somehow wrong".format(self.tagname)
    
class ExifError(Exception):
    """  Unknown error with Exif metadata.  """
    def __init__(self, except_inst):
        self.except_inst = except_inst
        
    def __str__(self):
        return "An error occured with Exif metadata :\n%s" % self.except_inst
    
