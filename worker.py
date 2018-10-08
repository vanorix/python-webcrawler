from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
import threading
import xmlrpc.client
import sys

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):
    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # print(newUrl)
                    # And add it to our colection of links:
                    self.links = self.links + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        # print(response)
        # print(response.getheader('Content-Type'))
        if response.getheader('Content-Type') == 'text/html; charset=UTF-8' or response.getheader('Content-Type') == 'text/html':
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlBytes = response.read()
            # print(response.getheaders())
            htmlString = htmlBytes.decode("utf-8")
            # print(htmlString)
            # print(htmlString)
            self.feed(htmlString)
            # print(self.links)
            return htmlString, self.links
        else:
            return "",[]

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, word, maxPages):  
    pagesToVisit = [url]
    foundWord = False

    # Start from the beginning of our collection of pages to visit:
    url = pagesToVisit[0]
    pagesToVisit = pagesToVisit[1:]
    try:
        parser = LinkParser()
        data, links = parser.getLinks(url)
        if data.find(word) > -1:
            foundWord = True
            # Add the pages that we visited to the end of our collection
            # of pages to visit:
            pagesToVisit = pagesToVisit + links
            print(" **Success!** ")
            return pagesToVisit
    except:
        print(" **Failed!** ", sys.exc_info())
    # if foundWord:
    #     print("The word", word, "was found at", url)
    # else:
    #     print("Word never found")

def enqueueUrls(future_work, prev_deepness, term):
	with xmlrpc.client.ServerProxy("http://localhost:3000/SOII") as proxy:
		for url in future_work:
			if (int(prev_deepness) - 1) >= 0:
				proxy.putWork(url, int(prev_deepness) - 1, term)

def main():
	with xmlrpc.client.ServerProxy("http://localhost:3000/SOII") as proxy:
		work = proxy.getWork()
		while True:
			# print(work)
			if(work == "Queue Empty!"):
				print("Queue Empty!")
			else:
				future_work = spider(work['url'], work['term'], int(work['deepness']))
				new_thread = threading.Thread(name='enqueueing', target=enqueueUrls, kwargs={'future_work': future_work, 'prev_deepness': work['deepness'], 'term': work['term']})
				new_thread.setDaemon(True)
				new_thread.start()
			work = proxy.getWork()

if __name__ == "__main__":
	main()