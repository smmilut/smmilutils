"""
    smmilutils.exif.exif
    Library for manipulation of exif image metadata
    
    started 2011-01-05
    by Pil Smmilut
    
"""
import datetime
import logging
## PIL = Python Image Library : for rotating image
# pretty standard, BUT can't write exif
from PIL import Image
#from PIL.ExifTags import TAGS
## pyexiv2: for read/write image metadata
import pyexiv2

import errors

#==============================================================================
global logger
logger = logging.getLogger("exif")

#------------------------------------------------------------------------------
def get_exif(filename):
    """  Get exif data from an image file.

        Returns a pyexiv2.metadata.ImageMetadata object

    """
    metadata = pyexiv2.ImageMetadata(filename)
    metadata.read()
    return metadata
    
#------------------------------------------------------------------------------
def get_exif_date(filename):
    """
          Get Exif date from an image filename.
        
        Returns a date object from the datetime module,
          which can be formatted like : exif_date.strftime("%Y-%m-%d_%Hh%Mm%Ss")
    """
    global logger
    # The name exif uses for the date of the image
    EXIF_DATE_TAGNAME = "Exif.Image.DateTime"
    ## Get all Exif metadata
    # (It would be faster if i knew how to get only one tag)
    exif_data = get_exif(filename)
    try:
        exif_datetag = exif_data[EXIF_DATE_TAGNAME]
    except KeyError:
        ## Exif tag is not in dictionnary
        logger.error("{0} : file does not contain Exif tag for date: {1}.".format(
                            filename, EXIF_DATE_TAGNAME))
        raise errors.NoExifTagError(EXIF_DATE_TAGNAME, filename)
    exif_date = exif_datetag.value
    logger.debug("{0} : Exif date retrieved : {1}".format(filename, exif_datetag))
    return exif_date
    
#------------------------------------------------------------------------------
def get_exif_oriented(filename):
    """
          Up-turn an image according to Exif metadata
        
        Returns a tuple (image object rotated upside-up, new metadata)
            or (None, None) if image was not transformed
    """
    global logger
    # The name used by Exif for the orientation of an image
    EXIF_ORIENT_TAGNAME = "Exif.Image.Orientation"
    ## Transformation necessary for straightening each orientation
    EXIFORIENT_TRANSFO = {
            # {Orientation: (method, argument, flipfunction)}
            '1': (None, None, None),  # 1: no need to change
            '2': ('transpose', Image.FLIP_LEFT_RIGHT, lambda x, y: (x, y)),
            '3': ('transpose', Image.ROTATE_180, lambda x, y: (x, y)),
            '4': ('transpose', Image.FLIP_TOP_BOTTOM, lambda x, y: (x, y)),
            '5': (None, None),  # 5: ROTATE_90 + FLIP_TOP_BOTTOM : i don't want to do it
            '6': ('transpose', Image.ROTATE_270, lambda x, y: (y, x)),
            '7': (None, None),  # 7: ROTATE_90 + FLIP_LEFT_RIGHT : i don't want to do it
            '8': ('transpose', Image.ROTATE_90, lambda x, y: (y, x))}
    # Names of transformations (only needed for logging)
    TRANS_NAMES = {
            Image.FLIP_LEFT_RIGHT: "flip left to right",
            Image.FLIP_TOP_BOTTOM: "flip top to bottom",
            Image.ROTATE_90: "rotate 90 degrees",
            Image.ROTATE_180: "rotate 180 degrees",
            Image.ROTATE_270: "rotate 270 degrees"}
    ## tags that might need to be updated
    ETAG_XSIZE = 'Exif.Photo.PixelXDimension'
    ETAG_YSIZE = 'Exif.Photo.PixelYDimension'
    # Get all Exif metadata
    exif_data = get_exif(filename)
    try:
        ## Get orientation (a number between 1 and 8)
        exif_orient = exif_data[EXIF_ORIENT_TAGNAME].raw_value
    except KeyError:
        ## Exif tag is not in dictionnary
        logger.error("{0} : file does not contain Exif tag '{1}'".format(
                            filename, EXIF_ORIENT_TAGNAME))
        raise errors.NoExifTagError(EXIF_ORIENT_TAGNAME, filename)
    try:
        ## Get the geometrical tranformation for straightening the image
        trans, trans_arg, flipf = EXIFORIENT_TRANSFO[exif_orient]
    except KeyError:
        ## Wrong orientation format
        logger.error("{0} : Exif tag '{1}' has unknown value '{2}'".format(
            filename, EXIF_ORIENT_TAGNAME, exif_orient))
        raise errors.BadExifTagError(EXIF_ORIENT_TAGNAME, filename)
    if trans is None:
        ## We don't have/need a method for tranforming the image
        # Don't transform the image
        logger.debug("{} : image was not transformed".format(filename))
        return (None, None)
    try:
        ## Open image for tranformation
        pil_image = Image.open(filename)
    except IOError:
        ## PIL could not open the image file
        logger.error("{} : Could not open image file".format(filename))
        raise errors.PIL_OpenError(filename)
    ## Transform the image
    new_image = getattr(pil_image, trans)(trans_arg)
    ## transform metadata if necessary
    try:
        ## Get xsize (in pixels)
        xsize = exif_data[ETAG_XSIZE]
    except KeyError:
        ## Exif tag is not in dictionnary
        logger.error("{0} : file does not contain Exif tag '{1}'".format(
                            filename, ETAG_XSIZE))
        raise errors.NoExifTagError(ETAG_XSIZE, filename)
    try:
        ## Get ysize (in pixels)
        ysize = exif_data[ETAG_YSIZE]
    except KeyError:
        ## Exif tag is not in dictionnary
        logger.error("{0} : file does not contain Exif tag '{1}'".format(
                            filename, ETAG_YSIZE))
        raise errors.NoExifTagError(ETAG_YSIZE, filename)
    # Swap the values of XResolution and YResolution if needed
    exif_data[ETAG_XSIZE], exif_data[ETAG_YSIZE] = flipf(xsize.value, ysize.value)
    # consider yourself ORIENTED, baby
    exif_data[EXIF_ORIENT_TAGNAME] = 1

    logger.debug("{0} : image was transformed: {1}".format(
                filename, TRANS_NAMES[trans_arg]))
    return new_image, exif_data
    
#------------------------------------------------------------------------------
def apply_new_exif(filename, new_exif):
    """  Change image metadata
        Put "new_exif" metadata into "filename" image
    """
    # Get original metadata
    old_exif = pyexiv2.ImageMetadata(filename)
    old_exif.read()
    # Replace original metadata with new one
    new_exif.copy(old_exif, exif=True)
    old_exif.write()

#==============================================================================
if __name__ == "__main__":
    # Some tests
    filename = "/home/shares/test/progtests/IMG_1834.JPG"
    exif_date = get_exif_date(filename)
    # Format the datetime object into a string
    formatteddate = exif_date.strftime("%Y-%m-%d_%Hh%Mm%Ss")
    print filename, "->", exif_date, "->", formatteddate
    # rotate if needed
    img_straight, new_exif = get_exif_oriented(filename)
    newname = "{0}_straightnow.JPG".format(filename)
    img_straight.save(newname)
    apply_new_exif(newname, new_exif)

