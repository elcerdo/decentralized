# coding=utf8
#A module for various stuff that doesn't fit elsewhere
#should be mostly test or temporary things

def open_pickle(filename,default):
    import cPickle
    try:
        return cPickle.load(open(filename))
    except (IOError,ValueError):
        return default

def get_classifiers():
    import re
    import os
    return [module[:-3] for module in os.listdir('classifiers') if re.search('_class\.py$',module)]

feeds=["http://digg.com/rss/index.xml","http://reddit.com/r/all/.rss","http://www.lemonde.fr/rss/sequence/0,2-3208,1-0,0.xml","http://linuxfr.org/backend/news-homepage/rss20.rss","http://del.icio.us/rss/","http://www.lefigaro.fr/rss/figaro_actualites.xml","http://news.ycombinator.com/rss","http://linuxfr.org/backend/journaux/rss20.rss","http://www.lepoint.fr/content/system/rss/a_la_une/a_la_une_doc.xml","http://rss.feedsportal.com/c/568/f/7295/index.rss","http://www.marianne2.fr/xml/syndication.rss","http://syndication.lesechos.fr/rss/rss_une.xml","http://blogs.lexpress.fr/attali/index.xml","http://feeds.feedburner.com/consommateur-si-tu-savais","http://www.reddit.com/r/AskReddit/","http://tempsreel.nouvelobs.com/file/rss_perm/rss_permanent.xml","http://top25.sciencedirect.com/rss.php?subject_area_id=17&journal_id=13618415","http://feedproxy.google.com/Phoronix","http://rss.feedsportal.com/c/499/f/413823/index.rss","http://www.slate.fr/rss.xml","http://www.mlyon.fr/rss/actu.php"]

def tokenize(text):
    import re
    text=re.sub(u"""[/1234567890=@\-#…«»”“’‘.!"'()*,:;<>?\[\]`{|}~&]"""," ",text).lower()
    return text.split()
