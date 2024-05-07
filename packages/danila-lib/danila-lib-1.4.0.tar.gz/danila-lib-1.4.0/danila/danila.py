import os

import cv2

from danila.danila_v1 import Danila_v1
from danila.danila_v2 import Danila_v2

"""main module for user"""


class Danila:
    """main class for user"""
    def __init__(self, version, yolov5_dir):
        if (version == 1):
            self.danila = Danila_v1(yolov5_dir)
        else:
            self.danila = Danila_v2(yolov5_dir)
    # returns string - class of rama using CNN network
    # img - openCV frame

    def rama_classify(self, img):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        return self.danila.rama_classify(img)

    # returns openCV frame with rama from openCV frame\
    def rama_detect(self, img):
        """rama_detect(img : openCV img) -> openCV image with drawn rama rectangle"""
        return self.danila.rama_detect(img)

    # returns openCV image with cut_rama
    def rama_cut(self, img):
        """rama_cut(img : openCV img) -> openCV image of rama rectangle"""
        return self.danila.rama_cut(img)

    #
    # returns openCV cut rama with drawn text areas
    def text_detect_cut(self, img):
        """returns openCV cut rama with drawn text areas"""
        return self.danila.text_detect_cut(img)

    # returns openCV img with drawn text areas
    def text_detect(self, img):
        """returns openCV img with drawn text areas"""
        return self.danila.text_detect(img)
    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def text_recognize(self, img):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        return self.danila.text_recognize(img)
