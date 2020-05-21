**The search engine is unavailable between 02:00 a.m. and 06:00 a.m. EST due to maintenance.**

Method slightly different to others.

Post request is made to download zip file, extracted and BN is stored.
BN is the suffix to the URLs which are to be scraped, easy to iterrate over all of them.

data which can be taken from extracted txt file:

* BN
* Name
* Address
* City
* State
* Country
* postcode

data which needs to be scraped from Canadian government site:

* charity website
* charity description

data which needs to be scraped from charity site:

* charity Email
* image url
* phone number
* social media links
* anything else which is missing from above

If charity type is going to be stored in the future problem may arise as this is stored on a different page than the one being scraped

TODO: clean up zip & text files after use