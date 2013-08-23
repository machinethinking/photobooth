import logging
import os
import sys
import time
from random import choice

class Photobooth(object):

    def __init__(self):
        self.new_pictures = []
        self.pics_from_camera = '0_pics_from_camera'
        self.archive_dir = '1_archive'
        self.production_dir = '2_production'
        self.loop_length = 5
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

    def move_to_archive(self):
        '''
        move self.new_pictures into the archive
        '''
        for file in self.new_pictures:
            try:
                os.link(self.pics_from_camera + "/" + file, self.archive_dir + "/" + file)
            except:
                pass

    def move_to_production(self):
        '''
        move files into production directory
        '''
        if len(self.new_pictures) < self.loop_length:
            num_photos_to_get = self.loop_length - len(self.new_pictures)
            logging.debug("num_photos_to_get:" , num_photos_to_get)
            archive_photos = []
            random_photos = []
            for root, dirs, files in os.walk(self.archive_dir):
                for file in files:
                    archive_photos.append(file)
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


def main(sleep_time):

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    p = Photobooth()
    p.verify_directories()

    while(True):
        p.get_new_pictures()
        if len(p.new_pictures) == 0:
            logging.debug("No new photographs")
            time.sleep(10)
            continue
        p.limit_new_pictures()
        p.move_to_archive()
        p.move_to_production()
        p.remove_new_photos()
        time.sleep(sleep_time)


if __name__ == "__main__":

    # sleep_time in seconds
    # 6 minutes = 360
    sleep_time = 30
    main(sleep_time)


