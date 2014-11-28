import urllib2
from bs4 import BeautifulSoup
import urlparse
import os

def get_pageurl(url):
    packtpub_url = "https://www.packtpub.com/all?search=&offset=&rows=48&sort="
    page = urllib2.urlopen(url)
    soup_packtpage = BeautifulSoup(page.read(), "lxml")
    page.close()
    next_page_data = soup_packtpage.find(text="Next").parent['data-offset']
    if next_page_data is None:
        next_page_url = None
    else:
        next_page_url = packtpub_url[:44] + next_page_data +  packtpub_url[-14:]   
        #next_page_url = re.sub("search=(.*)&", "search=" + next_page_data + "&", url)
    return next_page_url

def get_bookurls(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")
    page.close()
    books_div = soup.find_all(name='div', attrs = {"class":"book-block-outer", "itemprop":"mentions", "itemscope":"", "itemtype":"http://schema.org/Product"})
    url_base ='https://www.packtpub.com'
    urls = []
    for book_div in books_div:
        href = book_div.find('a')["href"]
        new_url = url_base + href
        #print new_url
        urls.append(new_url)
    return urls

def get_bookdetails(url):
    parsed_link = urlparse.urlsplit(url.encode('utf8'))
    parsed_link = parsed_link._replace(path=urllib2.quote(parsed_link.path))
    encoded_link = parsed_link.geturl()
    source = urllib2.urlopen(encoded_link).read()
    soup = BeautifulSoup(source, "lxml")
    isbn = soup.find(name = 'span', attrs = {"itemprop": "isbn"}).string
    soup_price=soup.find(name = 'div', class_="book-top-block-info left") 
    #print soup_price
    ebook_price = soup_price.find(name = 'div', class_="book-top-pricing-main-ebook-price").string.strip()
    book_price = soup_price.find(name = 'div', class_ ="book-top-pricing-main-book-price").string.strip()
    return isbn, float(ebook_price[1:]), float(book_price[1:])

def get_price_amazon(isbn):
    url_amazon = "http://www.amazon.com/s/ref=nb_sb_noss/181-3892143-3510445?url=search-alias%3Daps&field-keywords="
    url = url_amazon + isbn
    source = urllib2.urlopen(url).read()
    soup = BeautifulSoup(source)
    price = soup.find(name = 'span', class_ = "bld lrg red")
    if price:
        price = float(price.string.strip()[1:])
    else:
        price = None
    return price
    
def main():
    url = "https://www.packtpub.com/all?search=&offset=&rows=48&sort="
    #items = list()
    if os.path.exists("price.txt"):
        os.remove("price.txt")
    x = 1
    while x:
        try:
            price_file = open("price.txt", "a")
            new_url = get_pageurl(url)
            books_url = get_bookurls(url)
            for book_url in books_url:
                try:
                    isbn, ebook_price, book_price= get_bookdetails(book_url)
                    amazon_price = get_price_amazon(isbn)
                    price_file.write(isbn + '\t' + str(ebook_price) + '\t' + str(book_price) + '\t' + str(amazon_price) + '\n')
                    #items.append((isbn, ebook_price, book_price, amazon_price))
                    #print (isbn, ebook_price, book_price, amazon_price)                    
                except:
                    print "ERROR:\t"+ book_url
            price_file.close()
            url = new_url
        except Exception as e:
            print str(e)
            
if __name__ =="__main__":
    main()