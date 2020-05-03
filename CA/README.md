Method slightly different to others.

Post request is made to download zip file, extracted and BN is stored.
BN is the suffix to the URLs which are to be scraped, easy to iterrate over all of them.

Problem arises as two URLs are to be scraped for each charity and requests are completed in no set order.

TODO: Flask