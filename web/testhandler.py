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
    story_template="""<a href="/story/%s">%s</a> %d hits, %d symbols [%.50s]"""
    stories=sql.request("select url_md5,url,hit_count,symbol_count,symbols from story where not isnull(symbols) and not symbol_count=0 order by fetch_date asc limit 10")
    return template % "<br/>".join([story_template % (story[0],saxutils.escape(story[1]),story[2],story[3],saxutils.escape(story[4])) for story in stories])

def html_recommended_stories(session):
    template="""<div class="recommended_stories"><h1>recommended stories:</h1><p>%s</p></div>"""
    recommended_story_template="""<form method="post" action=""><a href="%s" class="view_it">view it</a> <input type="submit" class="good" value="good" name="rating"/> <input type="submit" class="bad" value="bad" name="rating"/> <a href="/story/%s">%s</a> <span class="rating">%.2f</span><input type="hidden" name="story_id" value="%d"/></form>"""
    recommended_stories=sql.request("select story.url_md5, story.url, recommended_story.computed_rating, story.id from story, recommended_story, kolmognus_user\
        where recommended_story.user_id=kolmognus_user.id and recommended_story.story_id=story.id\
        and kolmognus_user.login=%s and recommended_story.user_rating='?'\
        order by recommended_story.computed_rating desc\
        limit 10",session['login'])
    return template % "<br/>".join([recommended_story_template % (saxutils.escape(story[1]),story[0],saxutils.escape(story[1]),story[2],story[3]) for story in recommended_stories])

def html_rated_stories(session):
    template="""<div class="rated_stories"><h1>rated stories:</h1><p>%s</p></div>"""
    rated_story_template="""<a href="/story/%s">%s</a> <span class="rating">%s</span>"""
    rated_stories=sql.request("select story.url_md5, story.url, recommended_story.user_rating from story, recommended_story, kolmognus_user\
        where recommended_story.user_id=kolmognus_user.id and recommended_story.story_id=story.id\
        and kolmognus_user.login=%s and not recommended_story.user_rating='?'",session['login'])
    return template % "<br/>".join([rated_story_template % (story[0],saxutils.escape(story[1]),story[2]) for story in rated_stories])

def rate_story(param,session):
    rating_translation={'good':'G', 'bad':'B'}
    if session.has_key('login') and param.has_key('rating') and param.has_key('story_id'):
        sql.query("update kolmognus_user, recommended_story set recommended_story.user_rating=%s\
            where kolmognus_user.id=recommended_story.user_id and kolmognus_user.login=%s and recommended_story.story_id=%s", (rating_translation[param["rating"]],session['login'],param['story_id']))

def handler(request):
    welcome="""<div class="welcome"><p>Welcome to KolmoGNUS, the bayesian classifier that finds cool links for YOU</p></div>"""
    param,session=common.init_request(request)
    rate_story(param,session)

    header=''
    header+=common.html_session(param,session,request)
    header+=common.html_menu()

    main_frame=''
    if session.has_key('login'): #user logged in
        main_frame+=html_recommended_stories(session)
        main_frame+=html_rated_stories(session)
    else:
        main_frame+=welcome
    main_frame+=html_feeds()
    main_frame+=html_stories()
    main_frame+=html_users()

    footer=''
    footer+=common.html_debug(param,request)

    request.write(common.html_page(header,main_frame,footer).encode('utf-8'))
    return apache.OK
