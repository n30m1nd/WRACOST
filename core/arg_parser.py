#-*- coding: utf-8 -*-

import argparse

__author__ = 'n30'

class ArgumentParser():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Web Race Condition and Stress Tester')
        self.args = self.parse_args()

        if self.args.args and not self.args.params:
            exit("[-] Can't use --args without -p argument.")
        if self.args.v >= 2:
            print "[i] There are only 2 verbosity levels, sorry."
        pass

    def parse_args(self):
        self.parser.add_argument('url', help='url to test')
        self.parser.add_argument('method', help='request method (http://www.w3.org/Protocols/HTTP/Methods.html).')
        self.parser.add_argument('threads', type=int, help='Number of threads/connections to use.')
        self.parser.add_argument('-p', '--param', type=str, nargs='+', default=None,
                                 help='params to inject values into.')
        self.parser.add_argument('--args', type=str, nargs='+', default=None,
        help='''Values for the params -
        If the number of values doesn't match the number of params, the value assigned to each param will be randomized.''')
        self.parser.add_argument('-v', action='count', default=0, help='be verbose')
        return self.parser.parse_args()

    def get_arg(self, arg_name):
        return eval('self.args.'+arg_name) #fYeah! eval, shit bricks bruh