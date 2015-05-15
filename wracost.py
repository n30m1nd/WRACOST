#-*- coding: utf-8 -*-

__author__ = 'n30'

import httplib
from urlparse import urlparse
import threading
import sys
from WRACOST.core import arg_parser

class WRACOST():

    def __init__(self, url, method, verbosity, params=None, args=None):
        #   Set the command line arguments  #
        self.arg_url = url
        self.arg_method = method
        self.arg_verbosity = verbosity
        self.arg_param = params
        self.arg_args = args

        #   Useless if this class is used for any other programs    #
        self.lock = threading.Lock()

    def do_request(self, method=None, url=None):
        if not (method):
            method = self.arg_method
        if not (url):
            url = self.arg_url
        try:
            #   We need to do as few things as we can here  #
            parsed_url = urlparse(url)
            connection = httplib.HTTPConnection(parsed_url.hostname, parsed_url.port)
            connection.request(method, parsed_url.path)
            #   End of critical fastness hyperspeed section #

            self.lock.acquire()
            sys.stdout.write("[+] Request sent ")
            if (arg_verbosity > 0):
                response = connection.getresponse()
                print "to: ", arg_url
                print "[+]\tmethod:", arg_method
                print "[+]\tresponse headers: "
                for thing, thong in response.getheaders():
                    print "[+]\t\t",thing,': ',thong
            self.lock.release()
            connection.close()
        except httplib.HTTPException as ex:
            self.lock.acquire()
            print "[-] Connection error"
            print "[-] Err info: ", ex.message
            self.lock.release()
        except Exception as ex:
            self.lock.acquire()
            print "[-] Error"
            print "[-] Err info: ", str(ex)
            self.lock.release()

    def run(self, lock):
        self.lock = lock
        self.do_request()

if __name__ == '__main__':
    #   Set the command line arguments  #
    parser = arg_parser.ArgumentParser()
    arg_url = parser.get_arg('url')
    arg_nthreads = parser.get_arg('threads')
    arg_verbosity = parser.get_arg('v')
    arg_method = parser.get_arg('method')
    arg_param = parser.get_arg('param')
    arg_args = parser.get_arg('args')
    #   End of setting the arguments    #
    wracost = WRACOST(arg_url, arg_method, arg_verbosity, arg_param, arg_args)

    print('[+] Starting requests')
    #   Call arg_nthreads threads       #
    if (arg_verbosity > 0):
            print '[+]\t\tURL: ', arg_url
            print '[+]\t\tThreads: ', arg_nthreads
    else:
        ':'

    threads = []
    for i in range(arg_nthreads):
        lock = threading.Lock()
        t = threading.Thread(target=wracost.run, args=(lock,))
        threads.append(t)
        t.start()
