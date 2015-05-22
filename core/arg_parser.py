#-*- coding: utf-8 -*-

import argparse

__author__ = 'n30'

class ArgumentParser():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Web Race Condition and Stress Tester")
        self.args = self.parse_args()

        if self.args.payloads and not self.args.params:
            exit("[-] Can't use --params without --payloads argument.")
        if self.args.v >= 2:
            print "[i] There are only 2 verbosity levels, sorry."
        pass

    def parse_args(self):
        self.parser.add_argument("url", help="Url to test")
        self.parser.add_argument("method", help="Request method (http://www.w3.org/Protocols/HTTP/Methods.html).")
        self.parser.add_argument("threads", type=int, help="Number of threads/connections to use.")
        self.parser.add_argument("--params", type=str, nargs="+", default=None,
                                 help="Params to inject values into.")
        self.parser.add_argument("--payloads", type=str, nargs="+", default=None,
        help="""Values for the params -
        If the number of values doesn't match the number of params, the value assigned to each param will be randomized\
        .""")
        self.parser.add_argument("--cfile", help="Load cookie from this file. "+
                                                 "COOKIE FILE FORMAT: this=is;a=valid;for=mat;")
        self.parser.add_argument("-v", action="count", default=0, help="Be verbose")
        return self.parser.parse_args()
