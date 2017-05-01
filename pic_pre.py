# coding:utf-8
import imghdr
import os
from PIL import Image
import shutil

def copy_dir(path, new_path):
    items = os.listdir(path)
    num_pics = len(items)
    path_copy = new_path
    try:
        shutil.copytree(path, path_copy)
    except Exception, e:
        print 'Copy failed!'
        return 0
    copy_pics = len(os.listdir(path_copy))
    if num_pics == copy_pics:
        print "Copy successful!"
        print "%d pics copys" %(copy_pics)
    else:
        print 'Copy failed!'

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
        print "Renamed failed!"
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
                print "Covert to JPEG successful!"
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

# set up path_unpre and new_dir, run it!
path_unpre = '/home/johnny/Data/sohu_image_context/data/NewsInfo_6/image_copy'
new_dir = 'pic_test'
gan = path_unpre.rfind('/')
new_path = path_unpre[:gan+1] + new_dir
copy_dir(path_unpre, new_path)
convert_pic(new_path)