"""A python package that enhances speed and simplicity of parsing robots files."""

import requests
from .utils import _regex
from .utils import parser
from .utils.exceptions import *

__version__ = "1.0"
__description__ = "A python package that enhances speed and simplicity of parsing robots files."
__author__ = "xyzpw"
__license__ = "MIT"

def getRobots(url: str, find_url: bool = False, **kwargs) -> dict:
    """Returns a website's robots file contents.

    :param url:      the url which points to the robots file
    :param find_url: attempts to find the default robots location

    :kwargs: additional arguments for `requests.get` function"""
    if find_url:
        url = getRobotsUrl(url)
    contents = requests.get(url, **kwargs).text
    return parser.getRobotsInfo(contents)

def getRobotsUrl(link: str) -> str:
    """Returns the default robots location for a website.

    :param link: any uri of which will be replaced to the robots location"""
    url = _regex.searchForGroup(r"^(?P<url>https?://[a-z0-9\-\.]+?)(?<=[a-z0-9])(?:(?!\-\.)$|/.*?$)", link, "url")
    if url != None and "." in url:
        return "%s/robots.txt" % url

def getRobotsObject(url: str, find_url: bool = False, **kwargs):
    """Creates an object which contains robots information.

    :param url:      the url of which will be used to parse the robots file contents
    :param find_url: attempts to find the default robots location
    :kwargs: additional arguments to `requests.get` function"""
    if find_url:
        url = getRobotsUrl(url)
    pageContents = requests.get(url, **kwargs).text
    return parser.Robots(pageContents)

def getSitemap(url: str, find_url: bool = False, **kwargs) -> dict:
    """Returns information of a sitemap file.

    :param url: the url which points to the sitemap information
    :param find_url: attempts to find the default sitemap location
    :kwargs: additional arguments to `requests.get` function"""
    if find_url:
        url = getSitemapUrl(url)
        if not bool(url): return
        urlContents = requests.get(url, **kwargs).text
        sitemapInfo = parser.getXmlSitemapInfo(urlContents)
    else:
        urlContents = requests.get(url, **kwargs).text
        sitemapInfo = parser.getXmlSitemapInfo(urlContents)
    return sitemapInfo

def getSitemapUrl(link: str, verify: bool = True, **kwargs) -> str:
    """Returns the default sitemap location for a website.

    :param link: any uri of which will be replaced to the robots location
    :param verify: verifies that the sitemap location contains a sitemap file
    :kwargs: additional arguments to `requests.get` function"""
    sitemapLocation = _regex.searchForGroup(r"^(?P<url>https?://[a-z0-9\-\.]+?)(?<=[a-z0-9])(?:(?!\-\.)$|/.*?$)", link, "url")
    if sitemapLocation == None:
        return
    elif verify:
        robotsLocation = getRobotsUrl(link)
        sitemapResponse = getRobots(robotsLocation, find_url=True, **kwargs)
        if bool(sitemapResponse):
            sitemapResponse = sitemapResponse.get("sitemaps")
            return sitemapResponse[0] if bool(sitemapResponse) else None
        return
    else:
        return sitemapLocation + "/sitemap.xml"
