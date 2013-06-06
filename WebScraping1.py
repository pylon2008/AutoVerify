# coding=utf-8

import sys
import mechanize
import cookielib
from bs4 import BeautifulSoup
BASE_URL = "http://finance.sina.com.cn/"
##BASE_URL = "http://www.baidu.com/"

def scrape_links(base_url, data):
    """
    Scrape links pointing to article pages
    """
    soup = BeautifulSoup(data, from_encoding="gbk")

    # Create mechanize links to be used
    # later by mechanize.Browser instance
    #soup = BeautifulSoup(data)
    print 'scrape_links before'
    links = []
    for anchor in soup.find_all('a'):
        url = anchor['href']
        text = anchor.string
        shtml = '.shtml'
        thisYear = '2013'
        isWant = ( anchor.has_attr('href')) \
                 and ( anchor.has_attr('target') ) \
                 and (BASE_URL in url) \
                 and (shtml in url) \
                 and (text != None) \
                 and (thisYear in url)
        if isWant==True:
            unicode_string = (unicode(anchor.string))
            print 'unicode_string:',unicode_string
            print 'type(text): ', type(text)
            print 'type(unicode_string): ', type(unicode_string)
            tag = anchor.name

            attrs = []
            for name in anchor.attrs:
                attrs.append(name)
            link = mechanize.Link(base_url, url, text, tag, attrs)
            print link
            links.append(link)
        if len(links) > 10:
            break;
    print 'scrape_links after'
    return links
      
def scrape_articles(data, url):
    """
    Scrape the title and url of all the articles in this page
    """
    soup = BeautifulSoup(data, from_encoding="gbk")
    unicode_string = (unicode(soup.title.string))
    
    article = []
    article.append(url)
    article.append(unicode_string)

    return article

def main():
    """
    Get article network main page and follow the links
    to get the whole list of articles available
    """
    articles = []

    # Get main page and get links to all article pages
    
    br = mechanize.Browser()
    br.set_cookiejar(cookielib.LWPCookieJar())
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 

    # Want debugging messages?
##    br.set_debug_http(True)
##    br.set_debug_redirects(True)
##    br.set_debug_responses(True)


    
    request = br.open(BASE_URL)
    data = request.get_data()
     
    links = scrape_links(BASE_URL, data)


    # Scrape articles in linked pages
    for link in links[0:]:
        data = br.follow_link(link).get_data()
        articles.append(scrape_articles(data, link.url))
        br.back()

    # Ouput is the list of titles and URLs for each article found
    print ("Article Networkn"
    "---------------")
    for article in articles:
        print 'Url: ', article[0]
        print 'Title: ', article[1]
        print '\r\n\r\n'

if __name__ == "__main__":
    main()
