#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 gnunez88
#
# Distributed under terms of the MIT license.

"""
Unit test cases for morse.py
"""

import pytest
import sys

sys.path.append('..')
from morse import morse

def test_t2m_char():
    pass

# Argparse functions
def test_t2m_char_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, default='a')
    parser.add_argument('-m', '--to-morse', action='store_true', default=True)
    return parser.parse_args()

def main():
    #morse = __import__('morse')
    pass

if __name__ == '__main__':
    main()
