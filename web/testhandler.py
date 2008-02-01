from mod_python import apache
from web import sql

def handler(req):
    req.content_type='text/plain'

    logins=sql.login_list()
    feeds=sql.feed_list()
    services=sql.service_list()

    req.write('kolmognus info:\n')
    req.write('\tusers: '+' '.join(logins)+'\n')
    req.write('\tfeeds:\t'+'\n\t\t'.join(feeds)+'\n')
    req.write('\n')
    
    req.write('service:\n')
    req.write('\t'+'\n\t'.join(["%s: %s" % service for service in services])+'\n')
    req.write('\n')

    feed_fetched_count=sql.request('select hit_count from feed')
    req.write('cache:\n')
    req.write('\tcached urls for %d feed, total %d feed fetching\n' % (len(feed_fetched_count),sum([count[0] for count in feed_fetched_count]))) 
    return apache.OK
