import logging
import os
import sys
import time
from random import choice

class Photobooth(object):

    def __init__(self, loop_length):
        self.new_pictures = []
        self.archive_photos = []
        self.stock_photos = []
        self.pics_from_camera = '0_pics_from_camera'
        self.archive_dir = '1_archive'
        self.production_dir = '2_production'
        self.stock_dir = "stock_photographs"
        self.loop_length = loop_length
        self.debug = 1

    def get_new_pictures(self):
        self.new_pictures = []
        for root, dirs, files in os.walk(self.pics_from_camera):
            for file in files:
                if ".tmp_" in file:
                    continue
                self.new_pictures.append(file)
        logging.debug("new pictures")
        logging.debug(self.new_pictures)

    def limit_new_pictures(self):
        '''
        limit number of new photos to length of self.loop_length
        '''
        self.new_pictures = self.new_pictures[:self.loop_length]

    def link_to_archive(self):
        '''
        link self.new_pictures into the archive
        '''
        for file in self.new_pictures:
            try:
                os.link(self.pics_from_camera + "/" + file, self.archive_dir + "/" + file)
            except:
                pass


    def get_archive_photos(self):
        '''
        this should be generalized
        '''
        self.archive_photos = []
        if len(self.new_pictures) < self.loop_length:
            num_photos_to_get = self.loop_length - len(self.new_pictures)
            for root, dirs, files in os.walk(self.archive_dir):
                for x in range(num_photos_to_get):
                    try:
                        photograph = choice(files)
                    except:
                        continue
                    if photograph not in self.archive_photos:
                        self.archive_photos.append(photograph)

    def get_stock_photos(self):
        '''
        this should be generalized. see above
        '''
        self.stock_photos = []
        if (len(self.new_pictures) + len(self.archive_photos)) < self.loop_length:
            num_photos_to_get = self.loop_length - (len(self.new_pictures) + len(self.archive_photos))
            for root, dirs, files in os.walk(self.stock_dir):
                for x in range(num_photos_to_get):
                    photograph = choice(files)
                    if photograph not in self.archive_photos:
                        self.stock_photos.append(photograph)


    def link_to_production(self):
        '''
        link files into production directory
        '''
        for x in range(num_photos_to_get):
            random_photos.append(choice(archive_photos))
        for file in random_photos:
            os.link(self.archive_dir + "/" + file, self.production_dir + "/" + file)

        for num, file in enumerate(self.new_pictures):
            '''
            The old files should exist in the production directory.
            Remove them and replace with new ones.
            Hopefully this never causes some terrbie race condition.
            xbmc seems to tolerate it.
            '''
            if os.path.exists(self.production_dir + "/" + "00" + str(num) + ".jpg"):
                    os.unlink(self.production_dir + "/" + "00" + str(num) + ".jpg")
            os.link(self.pics_from_camera + "/" + file, self.production_dir + "/" + "00" + str(num) + ".jpg")

    def remove_new_photos(self):
        '''
        The new files should be in the archive, so
        remove them from new photos dir
        '''
        for file in self.new_pictures:
            os.unlink(self.pics_from_camera + "/" + file)

    def verify_directories(self):
        '''
        Will not work properly if not invoked from same directory
        as script
        '''
        for dir in [self.pics_from_camera, self.archive_dir, self.production_dir]:
            if not os.path.isdir(dir):
                os.mkdir(dir)


def main(sleep_time, loop_length):

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    p = Photobooth(loop_length)
    p.verify_directories()

    while(True):
        p.get_new_pictures()
        p.limit_new_pictures()
        p.get_archive_photos()
        p.get_stock_photos()
        print "new ", p.new_pictures
        print "archive ", p.archive_photos
        print "stock ", p.stock_photos
        sys.exit(1)
        p.link_to_archive()
        p.link_to_production()
        p.remove_new_photos()
        time.sleep(sleep_time)


if __name__ == "__main__":

    # sleep_time in seconds
    # 6 minutes = 360
    sleep_time = 30
    loop_length = 10
    main(sleep_time, loop_length)


