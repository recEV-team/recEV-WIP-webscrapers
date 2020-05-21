take [2019 form 990 json](https://s3.amazonaws.com/irs-form-990/index_2019.json) and extract ein, objectID, etc from this. then iterate through using [990-xml-reader](https://github.com/jsfenfen/990-xml-reader) to collect all other data. Use charity site scraper to collect everything else.

repo is a mess, still considering which is the best way to handle all this data

TODO: Flask, get json, parse