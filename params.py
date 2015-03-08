'''
Created on 2015-03-09
@author: okovalev
'''

import argparse

def __create_parser():
    parser = argparse.ArgumentParser()
    return parser

def create_common_parser():
    parser=__create_parser()

    parser.add_argument('--username', help='Username', required=True)
    parser.add_argument('--password', help='password', required=True)
    return parser


