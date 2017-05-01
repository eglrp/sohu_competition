# coding:utf-8
import imghdr
import os
from PIL import Image

# delete the broken pics
def delete_pic(path):
    """
    :param path: path for the preprocessing dir 
    :return: an integer for pics left
    """
    num_remove, num_left = 0, 0
    items = os.listdir(path)
    for image in items:
        img_loc = path + '/' + image
        if imghdr.what(img_loc):
            num_left += 1
        else:
            os.remove(img_loc)
            num_remove += 1
    print "%d pics have been removed. %d pics left." %(num_remove, num_left)
    return num_left

# rename the pics for their image type
def rename_pic(path):
    """
    :param path: path for the preprocessing dir 
    :return: a tuple with two integers, one is number of jpeg pics, other is not jpeg pics
    """
    num_total = delete_pic(path)
    items = os.listdir(path)
    num_jpeg = 0
    num_nojpeg = 0
    for image in items:
        img_loc = path + '/' + image
        img_type = imghdr.what(img_loc)
        img_name = img_loc.split('.')[0] + '.' + img_type
        os.rename(img_loc, img_name)
        if img_type == 'jpeg':
            num_jpeg += 1
        elif img_type != 'jpeg':
            num_nojpeg += 1
    result = [num_jpeg, num_nojpeg]
    if num_total != (result[0] + result[1]):
        print "renamed failed!"
        return 0
    print '%d jpeg files and %d not jpeg files' %(num_jpeg, num_nojpeg)
    return result

# convert the no jpeg files into jpeg files
def convert_pic(path):
    """
    :param path: path for the preprocessing dir 
    :return: an interger means total pics after convert
    """
    num_jpeg, num_nojpeg = rename_pic(path)
    items = os.listdir(path)
    num_remove = 0
    for image in items:
        img_loc = path + '/' + image
        img_type = imghdr.what(img_loc)
        out_pic = img_loc.split('.')[0] + '.' + 'jpeg'
        if img_type != 'jpeg':
            try:
                # remember to convert the pics into RGB type
                Image.open(img_loc).convert('RGB').save(out_pic)
                os.remove(img_loc)
                num_remove += 1
                print "Covert to JPEG successfully!"
            except Exception, e:
                print "This format can not support!", img_loc

    print num_remove

    if num_nojpeg != num_remove:
        print 'Convert failed!'
        return 0

    # check for whether the files convert to jpeg
    items = os.listdir(path)
    nums = len(items)
    for image in items:
        img_loc = path + '/' + image
        img_type = imghdr.what(img_loc)
        if img_type != 'jpeg':
            print "Convert failed!"
            return 0
    print "Convert all successfully!"
    print "There are %d jpeg pics now" %(nums)

# change the location, run it
path_unpre = '/home/johnny/Data/sohu_image_context/data/NewsInfo_6/pic_example'
convert_pic(path_unpre)