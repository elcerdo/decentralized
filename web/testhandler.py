from mod_python import apache,util
from xml.sax import saxutils
import sql
import common    

def html_users():
    template="""<div class="users"><h1>%d user(s):</h1><p>%s</p></div>"""
    users=sql.login_list()
    return template % (len(users)," ".join(users))

def html_feeds():
    template="""<div class="feeds"><h1>recent feeds:</h1><p>%s</p></div>"""
    feed_template="""<a href="/feed/%s">%s</a> (%d hits)"""
    feeds=sql.request("select url_md5,url,hit_count from feed order by fetch_date asc limit 10")
    return template % "<br/>".join([feed_template % feed for feed in feeds])

def html_stories():
    template="""<div class="stories"><h1>recent stories:</h1><p>%s</p></div>"""
    story_template="""<a href="/story/%s">%.50s</a> %d hits, %d symbols [%.50s]"""
    stories=sql.request("select url_md5,url,hit_count,symbol_count,symbols from story where not isnull(symbol_count) and not symbol_count=0 order by fetch_date asc limit 10")
    return template % "<br/>".join([story_template % (story[0],saxutils.escape(story[1]),story[2],story[3],saxutils.escape(story[4])) for story in stories])

def handler(request):
    welcome="""<div class="welcome"><p>Welcome to KolmoGNUS, the bayesian classifier that finds cool links for YOU</p></div>"""
    request.content_type='application/xhtml+xml'
    #request.discard_requestuest_body()
    request.send_http_header()

    param=util.FieldStorage(request,keep_blank_values=True)

    header=''
    header+=common.html_session(param,request)
    header+=common.html_menu()

    main_frame=''
    main_frame+=welcome
    main_frame+=html_feeds()
    main_frame+=html_stories()
    main_frame+=html_users()

    footer=''
    footer+=common.html_debug(param,request)

    request.write(common.html_page(header,main_frame,footer).encode('utf-8'))
    return apache.OK
