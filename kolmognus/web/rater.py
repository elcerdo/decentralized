#!/usr/bin/env python

import sql
import classifier

if __name__ == '__main__':
    rerate_delay="0 00:00:01"
    stories=sql.request("select id,url_md5,url,symbols from story where addtime(fetch_date,'12:00:00') > now() and (not isnull(fetch_date)) and (isnull(rated_date) or addtime(rated_date,%s) < now())" , rerate_delay) #do not rerate old news
    users=sql.request("select id,login from kolmognus_user")
    classifiers={}
    alluser_info=classifier.get_alluser_info()
    for user_id,login in users: #rate stories for each user
        if not user_id in classifiers:
            classifiers[user_id]=classifier.BayesianClassifier(user_id,alluser_info)
            #classifiers[user_id]=classifier.DumbClassifier()
        classif=classifiers[user_id]
        for url_id,umd5,url,symbols in stories:
            rating=classif.rate(symbols.split())
            sql.query("insert into recommended_story (user_id,story_id,computed_rating)\
                values(%s,%s,%s)\
                on duplicate key update computed_rating=%s",(user_id,url_id,rating,rating))

    for url_id,umd5,url,symbols in stories: #mark stories as rated
        sql.query("update story set rated_date=now() where id=%s;",url_id)
    sql.db.close()
    import time
    print "INFO: (%s) rated %d stories for %d users" % (time.asctime(),len(stories),len(users))
