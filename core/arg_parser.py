#-*- coding: utf-8 -*-

import argparse
import re

__author__ = 'n30'

class WracostArgs():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Web Race Condition and Stress Tester")
        self.args = self.get_args()

        if (self.args.threads and (self.args.params or self.args.payloads)):
            """
            These args are incompatible because the threads specify how many concurrent requests are going to be made
            And the params/payloads also specify how many requests are going to be made depending on combinations
            """
            print "[-] Either specify the --threads or the --params/payloads arguments. Not both."
            exit()
        if (self.args.getreq):
            if not (re.search(r'^"', self.args.getreq)):
                print '[-] Please specify the --getreq argument within quotes. Example: "a=1&b=2&c=3".'
                exit ()
            self.args.getreq = self.parse_param_inline()
        else:
            self.args.getreq = {}
        if (bool(self.args.payloads) ^ bool(self.args.params)): #XOR
            print "[-] Can't use --params without --payloads argument or viceversa"
            exit()
        elif (self.args.payloads and self.args.getreq):
            print \
            "[W] the params with the same name specified in both payloads and getreq arguments will" \
            " be overriden with the values in the \"payloads\" arguments."
        if (self.args.v >= 2):
            print "[i] Consider piping output to a file. This verbosity level gets the sourcecode of the request..."
            __import__('time').sleep(2)

    def get_args(self):
        self.parser.add_argument("url",
        help="Url to test.")

        self.parser.add_argument("method",
        help="Request method (http://www.w3.org/Protocols/HTTP/Methods.html).")

        self.parser.add_argument("-t", "--threads", type=int,
        help="Number of threads/connections to run. Can't be used with --params/payloads args.")

        self.parser.add_argument("-p", "--params", type=str, nargs="+", default=None,
        help="Params to inject values into. Can't be used with --threads args.")

        self.parser.add_argument("-y", "--payloads", type=str, nargs="+", default=None,
        help="Values for the params - Example: -p foo bar -y 0:intofoo 0:intofoo2 1:intobar. This will make 2 requests"\
        " making combinations with the parameters until all parameters are used.")

        self.parser.add_argument("-g", "--getreq", type=str, default=None,
        help="Params specified in a GET request format: ?a=1&b=2&c=3. NOTE: If used with the params/payload arguments "\
        "the params that have the same name will be replaced with the values in the \"payloads\" arguments.")

        self.parser.add_argument("--cfile",
        help="Load cookie from this file. COOKIE FILE FORMAT: this=is;a=valid;for=mat;")

        self.parser.add_argument("-v", action="count", default=0,
        help="Be verbose. -v shows headers and params sent. -vv like -v plus outputs the sourcecode from the request")
        return self.parser.parse_args()

    def get_params_dict(self):
        # TODO: Make this work -> --params foo bar --payloads 0:a 0:aa 0:aaa 1:b 1:bb 2:c 2:cc 2:ccc
        # TODO: First result -> { foo : 'a', bar : 'b' }
        # TODO: Second -> { foo : 'aa', bar : 'bb' }
        # TODO: Third -> { foo : 'aaa', bar : 'b' }
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
                paramsdict = {}
                paramsdict.update(self.args.getreq)
                for j, key in enumerate(self.args.params):
                    paramsdict[key] = matchdict[j][i%numparamrepeat[j]]
                yield paramsdict

    def parse_param_inline(self):
        if (self.args.getreq):
            matches = re.findall(r'(?:\?|\&|)([^=]+)\=([^&]+)', self.args.getreq)
            mydict = {}
            for m in matches:
                mydict[m[0]] = m[1]
            return mydict
        else:
            return {}

if __name__ == "__main__":
    argsie = WracostArgs()
    gen = argsie.get_params_dict()
    for g in gen:
        print g
