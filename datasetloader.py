import os
import cv2 as cv2
import numpy as np

from enum import Enum
from random import shuffle


class pathtype(Enum):
    relative = 1
    absolute = 2


class datasetloader:
    def __init__(self, root, type):
        self.root = root
        if type == pathtype.relative:
            self.root = os.path.dirname(os.path.realpath(__file__)) + root
        elif type == pathtype.absolute:
            self.root = root

        self.labelPaths = []
        self.labelNames = []
        self.labelCount = 0

        for labelName in os.listdir(self.root):
            if labelName == '.DS_Store': continue
            temp = self.root + '/' + labelName
            if os.path.isdir(temp):
                self.labelNames.append([labelName, self.labelCount])
                self.labelCount = self.labelCount + 1

        for index in range(self.labelCount):
            path = self.root + '/' + self.labelNames[index][0]
            list = os.listdir(path)
            for name in list:
                if name == '.DS_Store': continue
                self.labelPaths.append(path + '/' + name)

        shuffle(self.labelPaths)
        self.size = len(self.labelPaths)
        self.currentIndex = 0

    def load(self, shape, dev, batch):

        images = []
        labels = []

        for index in range(batch):
            if index + self.currentIndex >= self.size:
                return (None, None)

            path = self.labelPaths[self.currentIndex + index]
            image = cv2.imread(path)
            npImage = np.array(image)
            npImage = npImage / dev
            npImage = npImage.flatten().reshape(shape)
            images.append(npImage)

            label = [0] * self.labelCount
            for index2 in range(self.labelCount):
                if self.labelNames[index2][0] in path:
                    label[self.labelNames[index2][1]] = 1
                    labels.append(label)

            if index + self.currentIndex >= self.size:
                break

        self.currentIndex += batch

        # print('current index =', self.currentIndex , '\n')
        return (images, labels)

    def clear(self):
        self.currentIndex = 0

    def label_count(self):
        return self.labelCount

    def sample_count(self):
        return self.size


