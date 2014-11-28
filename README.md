book_prices
===========
Using BeautifulSoup to compare book prices listed at PacktPub and Amazon

Basic steps:
1. Start from "https://www.packtpub.com/all?search=&offset=&rows=48&sort=";
2. Use "Next" to get all the next page links;
3. Use BeautifulSoup to find out all the book links in every page;
4. From the book links get all the book details: ISBN, ebook_price, book_price;
5. Use the ISBN from step 4 combined with http://www.amazon.com/s/ref=nb_sb_noss/181-3892143-3510445?url=search-alias%3Daps&field-keywords=
   to get price at Amazon
6. Save all the items into a file.
