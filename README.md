photobooth
==========

This photobooth software was designed to be used in a social setting. In batches, photographs taken 
are displayed in loop with a delay. When there are not enough new photographs to refill the
loop, previously taken photographs are randomly selected to fill the gap.

Requirements:
A camera connected via (probably) USB.
A program, like OSX Image Capture which will trigger the camera and download the picture
A person to trigger the photos
An external program to diplay the photos in a loop. I use xbmc.

Usage:
Set the loop_lenth and sleep_time in script as desired. A loop_lenth of 30 and sleep of 360 (6 minutes) seems to work well.
Set the camera software to dump photos into 0_pics_from_camera. Optionally dump in some photos or enjoy some pictures of kittens.
Start photobooth.py before xbmc. This is necessary because xbmc needs to have all the filenames at start of slide show.
Start an xbmc slideshow pointing at 2_production directory.
Take more photos, two drink minimum. New photos should show up in xbmc slideshow in a cycle or two.



