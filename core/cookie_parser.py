#-*- coding: UTF-8 -*-

__author__ = 'n30'

import cookielib
import re

class CookieParser(cookielib.FileCookieJar):

    #   TODO: Implement a method for FileCookieJar
    #   TODO: so we can use this class and the other
    #   TODO: filetypes that cookielib uses

    def parseOneLineCookie(self, cookiefromfile):
        matches = re.findall(r"\s*(.*?)=(.*?);",cookiefromfile)
        cookie_dict = {}
        for m in matches:
            cookie_dict[m[0]] = m[1]
        return cookie_dict

if __name__ == "__main__":
    #   TESTING PURPOSES ... Unit tests maybe?   #
    cparser = CookieParser()
    print cparser.parseOneLineCookie("coo=kie;mas=ter;fuck=ERY=E=))$`+ç´`()); this=oh lor d reeeek?=!'$=?ris;")
