'''
Desc:
File: /enum.py
File Created: Saturday, 29th July 2023 7:36:06 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
from enum import Enum


class Freq(Enum):
    YEAD = 'Y'
    QUARTER = 'Q'
    MONTH = 'M'
    WEEK = 'W'
    DAY = 'D'


class Scene(Enum):
    STATS = 'stats'
    MOMENTUM = 'momentum'
    TREND = 'trend'
