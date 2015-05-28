#-*- coding: utf-8 -*-

import argparse
import re

__author__ = 'n30'

class WracostArgs():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Web Race Condition and Stress Tester")
        self.args = self.get_args()

        if self.args.payloads and not self.args.params:
            exit("[-] Can't use --params without --payloads argument.")
        if self.args.v >= 2:
            print "[i] For now there are only 2 verbosity levels, sorry."
        pass

    def get_args(self):
        self.parser.add_argument("url", help="Url to test.")
        self.parser.add_argument("method", help="Request method (http://www.w3.org/Protocols/HTTP/Methods.html).")
        self.parser.add_argument("-t", "--threads", type=int, help="Number of threads/connections to use.")
        self.parser.add_argument("-p", "--params", type=str, nargs="+", default=None,
                                 help="Params to inject values into.")
        self.parser.add_argument("-y", "--payloads", type=str, nargs="+", default=None,
        help="""Values for the params - Rethink""")
        self.parser.add_argument("--cfile", help="Load cookie from this file. "+
                                                 "COOKIE FILE FORMAT: this=is;a=valid;for=mat;")
        self.parser.add_argument("-v", action="count", default=0, help="Be verbose.")
        return self.parser.parse_args()

    def get_params_dict(self):
        # TODO: Make this work -> --params foo bar --payloads 0:a 0:aa 0:aaa 1:b 1:bb 2:c 2:cc 2:ccc
        # TODO: First result -> { foo : 'a', bar : 'b' }
        # TODO: Second -> foo=winky&bar=whompy
        # TODO: Third -> foo=blinky&bar=st4:5:ompy
        paramsdict = {}
        matchdict = {}
        numparamrepeat = {}

        for payload in self.args.payloads:
            try:
                match = re.search(r'(^\d+):(.*)',payload)
                num_match = int(match.group(1))
                payl_match = match.group(2)

                if num_match in numparamrepeat:
                    numparamrepeat[num_match] = 1+numparamrepeat[num_match]
                else:
                    numparamrepeat[num_match] = 1
                if num_match not in matchdict:
                    matchdict[num_match] = []

                matchdict[num_match].append(payl_match)

            except AttributeError:
                print '[-] Wrong payload format:', payload
                exit()

        for i in range(max(numparamrepeat.values())):
                for j, key in enumerate(self.args.params):
                    paramsdict[key] = matchdict[j][i%numparamrepeat[j]]
                yield paramsdict


if __name__ == "__main__":
    argsie = WracostArgs()
    gen = argsie.get_params_dict()
    pass