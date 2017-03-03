"""
gethtml with cookies support  v1
by anarchintosh @ xbmcforums
Copyleft = GNU GPL v3 (2011 onwards)

this function is paired with weblogin.py
and is intended to make it easier for coders wishing
to scrape source of pages, while logged in to that site.

USAGE:
!!!!!First set the compatible_urllist below!!!!!!!!!

import gethtml

to load html without cookies
source = gethtml.get(url)

to load html with cookies
source = gethtml.get(url,'my-path-to-cookiefile')

"""

import urllib, urllib2
import cookielib
import os
import re

# !!!!!!!!!!! Please set the compatible_urllist
# set the list of URLs you want to load with cookies.
# matches bits of url, so that if you want to match www243.megaupload.com/ you
# can just put '.megaupload.com/' in the list.
compatible_urllist = ['watchslipstream.com/']
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

# COOKIES_PATH = os.path.join(__path__, 'cookies.txt')
COOKIES_PATH = 'cookies.txt'


def url_for_cookies(url):
    # ascertain if the url contains any of the phrases in the list. return True if a match is found.
    for compatible_url in compatible_urllist:
        if re.search(compatible_url, url):
            return True

    return False


def myget(url, query_data=None, extra_headers=None):
    cj = cookielib.MozillaCookieJar(COOKIES_PATH)
    cj.load()

    req = urllib2.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    if extra_headers:
        for k, v in extra_headers.iteritems():
            req.add_header(k, v)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    if isinstance(query_data, dict):
        query_data = json.dumps(query_data)

    response = opener.open(req, data=query_data)
    data = response.read()
    response.close()
    return data


def get(url, data=None, extra_headers=None, cookiepath=None):
    # print 'processing url: '+url
    # use cookies if cookiepath is set and if the cookiepath exists.
    if cookiepath is not None:

        # only use cookies for urls specified
        if url_for_cookies(url):

            # check if user has supplied only a folder path, or a full path
            if os.path.isdir(cookiepath):
                # if the user supplied only a folder path, append on to the end of the path a common filename.
                cookiepath = os.path.join(cookiepath, 'cookies.lwp')

            # check that the cookie exists
            if os.path.exists(cookiepath):
                cj = cookielib.LWPCookieJar()
                cj.load(cookiepath)

                req = urllib2.Request(url)
                req.add_header('User-Agent', USER_AGENT)

                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                response = opener.open(req, data=data)
                link = response.read()
                response.close()
                return link

    return _loadwithoutcookies(url)


def _loadwithoutcookies(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link
