#-*- coding: utf-8 -*-

__author__ = 'n30'

import httplib
from urlparse import urlparse
import threading
import sys
import requests
from WRACOST.core import arg_parser


class WRACOST():

    def __init__(self, url, method, verbosity, params=None, payloads=None, cookie=None):
        #   Set the command line arguments  #
        self.arg_url = url
        self.arg_method = method
        self.arg_verbosity = verbosity
        self.arg_params = params
        self.arg_payloads = payloads
        self.arg_cookie = cookie

        #   Useless if this class is used by any other files than this  #
        self.lock = threading.Lock()

    def parse_param_data(self):
            data_payload = {}
            if (self.arg_params and self.arg_payloads):
                for n, param in enumerate(self.arg_params):
                    if (len(self.arg_params) >= len(self.arg_payloads)):
                        data_payload[param] = self.arg_payloads[n % len(self.arg_payloads)]
            return data_payload

    def do_request(self, method=None, url=None):
        if not (method):
            method = self.arg_method
        if not (url):
            url = self.arg_url
        try:
            parsed_payload = self.parse_param_data()
            req_sent = ''
            #   POST or GET?    #
            #   We need to do as few things as we can here  #
            if (method == 'POST'):
                self.semaphore.acquire()
                req_sent =requests.post(url, data=parsed_payload)
            elif(method == 'GET'):
                self.semaphore.acquire()
                req_sent = requests.get(url)

            #   End of critical fastness hyperspeed section #

            self.lock.acquire()
            sys.stdout.write("[+]\tRequest sent ")
            if (arg_verbosity > 0):
                print "to:", arg_url
                print "[+]\t\tmethod:", arg_method
                if (self.arg_method!='GET'):
                    print "[+]\t\tpayload:", parsed_payload
            #    print "[+]\tresponse headers: "
            #    for thing, thong in response.getheaders():
            #        print "[+]\t\t", thing,': ', thong
            self.lock.release()

        except httplib.HTTPException as ex:
            self.lock.acquire()
            print "[-] Connection error: ", ex.message
            self.lock.release()
        except Exception as ex:
            self.lock.acquire()
            print "[-] Error: ", str(ex)
            self.lock.release()


    def run(self, lock, semaphore):
        self.lock = lock
        self.semaphore = semaphore
        self.do_request()

if __name__ == '__main__':
    #   Set the command line arguments  #
    parser = arg_parser.ArgumentParser()
    arg_url = parser.args.url
    arg_nthreads = parser.args.threads
    arg_verbosity = parser.args.v
    arg_method = parser.args.method
    arg_param = parser.args.params
    arg_payload = parser.args.payloads
    #   End of setting the arguments    #

    #   Init                            #
    #   Need to add: Arg cookie         #
    wracost = WRACOST(arg_url, arg_method, arg_verbosity, arg_param, arg_payload)

    print('[+] Starting requests...')

    if (arg_verbosity > 0):
            print '[+]\t\tURL: ', arg_url
            print '[+]\t\tThreads: ', arg_nthreads

    threads = []
    semaphore = threading.Semaphore(0)
    lock = threading.Lock()
    for i in range(arg_nthreads):
        t = threading.Thread(target=wracost.run, args=(lock, semaphore,))
        threads.append(t)
        t.start()

    print '[+] Damn semaphores, how do they work...?'
    # Wait for all threads to
    __import__('time').sleep(5)

    for i in range(arg_nthreads):
        semaphore.release()
