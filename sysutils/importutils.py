"""
    smmilutils.sysutils.importutils
    utilities for importing in custom ways
    
    Pil Smmilut 2011-02-15
    
"""

#==============================================================================
def simpleimport(fullmodname):
    """  Import a module from its name, like :
        import fullmodname
        
        fullmodname contains '.', like this: package.module.submodule
        
        I know it sounds complicated, but i tested,
          and that part of python just seems meh
        
    """
    ## Import the UPPERMOST module/package
    mod = __import__(fullmodname)
    ## Import all components of the path
    components = fullmodname.split('.')
    for comp in components[1:]:
        ## Descend the hierarchy and import
        mod = getattr(mod, comp)
    return mod
    
#------------------------------------------------------------------------------
def from_import(fullmodname, objname):
    """  Import an object from its name, and the name of its module, like :
        from fullmodname import objname
        
        fullmodname contains '.', like this: package.module.submodule
        
        I know it sounds complicated, but i tested,
          and that part of python just seems meh
        
    """
    ## Import the UPPERMOST module/package
    mod = __import__(fullmodname)
    ## Import all components of the path
    components = fullmodname.split('.')
    for comp in components[1:]:
        ## Descend the hierarchy and import
        mod = getattr(mod, comp)
    ## Lastly, import the object required
    obj = getattr(mod, objname)
    return obj
    
#==============================================================================
if __name__ == "__main__":
    a = simpleimport("os.path")
    print a
    b = from_import("smmilutils.simplegui.tk", "FilelistGUI")
    print b
    

