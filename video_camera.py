#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class VideoCamera(object):
    '''This class provides video frame stream for REST endpoint.'''

    def __init__(self, size):
        '''Constructor. Initializes video camera and sets frame width and height
        parameters.'''
        
        self.stream = cv2.VideoCapture(0)
        self.size = size
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, size)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, size / 2)
        self.frame = np.zeros((size, size, 3), dtype=np.uint8)

    def __del__(self):
        '''Destructor. Deinitializes video camera.'''

        self.stream.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        '''Reads frame from video camera, transforms it into hologram format and
        returns it encoded as JPG.'''

        success, frame = self.stream.read()
        for i in xrange(self.size / 2):
            part = frame[i, i:self.size - i - 1]
            part_flipped = cv2.flip(part, 0)
            np.copyto(self.frame[i, i:self.size - i - 1], part)
            np.copyto(self.frame[i:self.size - i - 1, i], part_flipped)
            np.copyto(self.frame[self.size - i - 1, i:self.size - i - 1],
                      part_flipped)
            np.copyto(self.frame[i:self.size - i - 1, self.size - i - 1], part)

        ret, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()
