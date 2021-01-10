import tkinter as tk
import os
import time
import datetime
from PIL import Image
from tkinter import filedialog
from pathlib import Path


valid_file_types = ['.jpg', '.JPG', '.png', '.PNG']


class DirNode:
    def __init__(self, path, level):
        self.name = os.path.basename(os.path.normpath(path))
        self.new_name = None
        self.path = path
        self.level = level
        self.img_files = list()
        self.sub_nodes = list()
        self.other_files = list()
        self.scan_files_in_node()

    def scan_files_in_node(self):
        names = os.listdir(self.path)
        imgs_names = list()
        dirs_names = list()
        other_names = list()
        for name in names:
            abs_path = os.path.join(self.path, name)
            if os.path.isdir(abs_path):
                dirs_names.append(DirNode(os.path.join(self.path, name), self.level + 1))
            elif os.path.isfile(abs_path):
                if get_file_ext(abs_path) in valid_file_types:
                    imgs_names.append(Photo(name, self.path))
                else:
                    other_names.append(name)
            else:
                pass
        self.img_files = imgs_names
        self.sub_nodes = dirs_names
        self.other_files = other_names

    def display_structure(self):
        print('%s images were found' % (self.count_all_images()))
        prefix = ''
        for i in range(0, self.level):
            prefix += ' > '
        print(prefix + '[ ' + self.name + ' ]')

        if len(self.img_files) > 0:
            print(prefix + '//images')
            for img in self.img_files:
                print(prefix + str(img.name) + ' --> ' + str(img.new_name))

        if len(self.other_files) > 0:
            print(prefix + '//others')
            for img in self.other_files:
                print(prefix + ' ' + img)

        print('')
        for node in self.sub_nodes:
            node.display_structure()

    def rename_all(self):
        for img in self.img_files:
            img.rename()
        for node in self.sub_nodes:
            node.rename_all()

    def count_all_images(self):
        count = len(self.img_files)
        for node in self.sub_nodes:
            count += node.count_all_images()
        return count


class Photo:
    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, self.name)
        self.root_path = path

        # get date from file name
        dates = list()
        try:
            # get foto taken date
            ttime = Image.open(self.path).getexif()[36867]
            dates.append(create_date_dict_from_xtime(ttime, 'taken'))
        except KeyError:
            pass

        # get foto last modfied date
        mtime = str(datetime.datetime.strptime(time.ctime(os.path.getmtime(self.path)), "%a %b %d %H:%M:%S %Y"))
        dates.append(create_date_dict_from_xtime(mtime, 'modified'))

        # get foto creation date
        mtime = str(datetime.datetime.strptime(time.ctime(os.path.getctime(self.path)), "%a %b %d %H:%M:%S %Y"))
        dates.append(create_date_dict_from_xtime(mtime, 'created'))

        # get date from name
        # TODO extract date from name
        dates.append(find_date_in_name(self.name))

        log('------')
        for d in dates:
            log(d.name)


        #self.date = ctime_dict
        #self.new_name = build_date_name(ctime_dict, get_file_ext(self.path))
        self.new_name = dates[0].name

    def rename(self):
        os.rename(self.path, os.path.join(self.root_path, self.new_name))


class DateAndTime:
    def __init__(self, year, month, day, hour, minute, second, date_type):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.min = minute
        self.sec = second
        self.dtype = date_type
        self.name = self.build_date_name()

    def build_date_name(self):
        scheme = '%s-%s-%s_%s-%s-%s_%s'
        date_name = scheme % (self.year, self.month, self.day, self.hour, self.min, self.sec, self.dtype)
        return date_name


def get_file_ext(abs_file_path):
    return os.path.splitext(abs_file_path)[-1]


def create_date_dict_from_xtime(t, dtype):
    return DateAndTime(t[0:4], t[5:7], t[8:10], t[11:13], t[14:16], t[17:19], dtype)



# root_path = Path(tk.filedialog.askdirectory())
# my_node = DirNode(root_path, 0)
# my_node.display_structure()
#my_node.rename_all()
