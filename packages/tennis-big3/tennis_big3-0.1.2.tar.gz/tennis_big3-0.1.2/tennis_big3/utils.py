#!/usr/bin/python3

from .players import big_three

def total_gs():

    print(f"The total Grand Slams between the Big-3 are {sum(titles.gs for titles in big_three)}")

