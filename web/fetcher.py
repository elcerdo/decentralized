#!/usr/bin/env python

import sql
import time

def has_enough_urls():
    return sql.request("select count(id) from story where rated_date is null")[0][0] > 100


if __name__ == '__main__':
    import delicious
    import time
    sql.service_set_status('fetcher','started')
    while True:
        #is incoming full??
        #build url list from recent and requested tags
        #fetch urls
        if not has_enough_urls(): 
            print "INFO: Fetch start"
            for url in delicious.get_recent_urls():
                print "INFO: Getting symbols"
                symbols = get_symbols_for_story(url)
                print "INFO: ",symbols
        else:
            print "INFO: fetcher waiting for more urls to be needed"
            time.sleep(60) 
