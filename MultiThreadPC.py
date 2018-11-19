#!/usr/bin/env python3
import time
import logging
import random
import threading
import cv2
import numpy as np
import base64
import queue

# filename of clip to load
filename = 'clip.mp4'

BUF_SIZE = 10

# shared queue
extractionQueue = queue.Queue(BUF_SIZE)
convertQueue = queue.Queue(BUF_SIZE)

# lock1 = threading.RLock()
# lock2 = threading.RLock()




class ProducerThreadExtract(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThreadExtract,self).__init__()
        self.target = target
        self.name = name

    def run(self):

        # Initialize frame count
        count = 0

        # open video file
        vidcap = cv2.VideoCapture(filename)

        # read first image
        success,image = vidcap.read()
        print("Extraction of frame {} {} ".format(count, success))
        while True:
            if not extractionQueue.full():

                # get a jpg encoded frame
                success, jpgImage = cv2.imencode('.jpg', image)

                #encode the frame as base 64 to make debugging easier
                jpgAsText = base64.b64encode(jpgImage)

                # add the frame to the buffer
                # lock1.acquire()
                extractionQueue.put(jpgAsText)
                # lock1.release()
                success,image = vidcap.read()
                print("Extraction of frame {} {} ".format(count, success))
                count += 1
                if not success:
                    break
        return

class ConsumerProducerThreadConvert(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerProducerThreadConvert,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        print("Started t2")
        count = 0
        while True:
            if not extractionQueue.empty():
                # load the next file
                # lock1.acquire()
                inputFrame = extractionQueue.get()
                # lock1.release()

                print("Converting frame {}".format(count))
                jpgRawImage = base64.b64decode(inputFrame)

                # convert the raw frame to a numpy array
                jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

                # get a jpg encoded frame
                img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
                # convert the image to grayscale
                grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # get a jpg encoded frame
                success, jpgImageGrey = cv2.imencode('.jpg', grayscaleFrame)

                #encode the frame as base 64 to make debugging easier
                jpgGreyAsText = base64.b64encode(jpgImageGrey)
                if not convertQueue.full():
                    # lock2.acquire()
                    # write output file
                    convertQueue.put(jpgGreyAsText)
                    # lock2.release()
                count += 1

        return


class ConsumerThreadDisplay(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThreadDisplay,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):

        # initialize frame count
        count = 0
        startTime = time.time()
        frameDelay   = 42
        while True:
            if not convertQueue.empty():
                # get the next frame
                # lock2.acquire()
                frameAsText = convertQueue.get()
                # lock2.release()
                # decode the frame
                jpgRawImage = base64.b64decode(frameAsText)

                # convert the raw frame to a numpy array
                jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

                # get a jpg encoded frame
                img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

                print("Displaying frame {}".format(count))

                # display the image in a window called "video" and wait 42ms
                # before displaying the next frame
                elapsedTime = int((time.time() - startTime) * 1000)
                # print("Time to process frame {} ms".format(elapsedTime))

                # determine the amount of time to wait, also
                # make sure we don't go into negative time
                timeToWait = max(1, frameDelay - elapsedTime)
                cv2.imshow("Video", img)
                if cv2.waitKey(timeToWait) and 0xFF == ord("q"):
                    break
                startTime = time.time()
                count += 1
        return


t1 = ProducerThreadExtract(name = 'T1')
t2 = ConsumerProducerThreadConvert(name = 'T2')
t3 = ConsumerThreadDisplay(name = 'T3')
t1.start()
t2.start()
t3.start()
