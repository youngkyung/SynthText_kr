import numpy as np
import matplotlib.pyplot as plt 
import scipy.io as sio
import os.path as osp
import random, os
import cv2
#import cPickle as cp
# import _pickle as cp
import pickle as cp
import scipy.signal as ssig
import scipy.stats as sstat
import pygame, pygame.locals
from pygame import freetype
#import Image
from PIL import Image
import math
from common import *


char_freq_path = 'mydata/models/char_freq.cp'
font_model_path = 'mydata/models/font_px2pt.cp'

with open(char_freq_path,'rb') as f:
    # u = cp.load(f)
    # u = pickle._Unpickler(f)
    # u = cp.Unpickler(f)
    # u.encoding = 'latin1'
    u = cp.load(f)

print(u)

with open(font_model_path,'rb') as f:
    # u = cp.load(f)
    # u = pickle._Unpickler(f)
    # u = cp.Unpickler(f)
    # u.encoding = 'latin1'
    u = cp.load(f)

# print(u)