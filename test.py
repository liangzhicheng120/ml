#!/bin/bash
# -*-coding=utf-8-*-
import re
import sys
import os
import MySQLdb
from ml.util.schemas import *
from ml.util.encrypt import *
from sys import argv
import traceback

if __name__ == '__main__':
    result = ''
    with open('html.txt', 'rb') as f:
        for line in f:
            result += line.strip()
    print result