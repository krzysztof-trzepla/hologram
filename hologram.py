#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

SIZE = 400

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, SIZE)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SIZE / 2)

codec = cv2.VideoWriter_fourcc('j', 'p', 'e', 'g')
out = cv2.VideoWriter()
out.open('output.avi', codec, 16.0, (SIZE, SIZE), True)
img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        for i in xrange(SIZE / 2):
            row = frame[i, i:SIZE - i - 1]
            rowFlipped = cv2.flip(row, 0)
            np.copyto(img[i, i:SIZE - i - 1], row)
            np.copyto(img[i:SIZE - i - 1, i], rowFlipped)
            np.copyto(img[SIZE - i - 1, i:SIZE - i - 1], rowFlipped)
            np.copyto(img[i:SIZE - i - 1, SIZE - i - 1], row)

        cv2.imshow('frame', img)
        out.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
