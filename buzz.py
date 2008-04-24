#!/usr/bin/env python
# coding=utf8
#Identify the latest trends on delicious

import os
import re
import cPickle
import time
import sys

SIGNIFICANCE_CONSTANT=1

def tokenize(text):
    text=re.sub(u"""[1234567890@#»”’.!"'()*,:;<>?\[\]`{|}~&]"""," ",text).lower()
    return text.split()
    
def add(dict,key):
    dict[key]=dict.get(key,0)+1

def get_feed_stories(feeds=["http://digg.com/rss/index.xml","http://reddit.com/r/all/.rss","http://www.lemonde.fr/rss/sequence/0,2-3208,1-0,0.xml","http://linuxfr.org/backend/news-homepage/rss20.rss","http://del.icio.us/rss/"]):
    import feedparser
    stories=[]
    for f in feeds:
        stories.extend(entry.title for entry in feedparser.parse(f).entries)
    return stories

def get_object_from_file(filename,default={}):
    try:
        f=open(filename) #we separate this from the rest of the stuff because this is the only critical piece of data
        mydict=cPickle.load(f)
        f.close()
    except IOError,e:
        print "already_seen file not found, creating a new one..."
        mydict=default
    return mydict

def show_original_stuff():
    now=time.time()
    already_seen=get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen.pck"))
    already_seen_links=get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen_links.pck"),set())
    try:
        f=open(os.path.expanduser("~/.popurls.pck"))
        time_fetched,story_ratings,cur=cPickle.load(f)
        f.close()
    except IOError,e:
        print "popurls file not found, creating a new one..."
        time_fetched,story_ratings,cur=0,None,[]
    if story_ratings is None or now-time_fetched>10 * 60: #if file is older than ten minutes
        all_stories=get_feed_stories()
        stories=[]
        for s in all_stories:
            if s not in already_seen_links:
                already_seen_links.add(s)
                stories.append(s)
        raw_text=" ".join(stories)
        if not stories: 
            print "No new stories found"
            import sys
            sys.exit()
        time_fetched=now
        current={}
        for m in tokenize(raw_text):
            add(current,m)
        cur=[]
        for k,count in current.items():
            if k in already_seen.keys():
                already_seen[k]=now,already_seen[k][1]+count #this word is still being seen
            else:
                if count>=SIGNIFICANCE_CONSTANT: #Discard low occurences, they don't represent a trend
                    cur.append((k,count))
        cur.sort(key=lambda e:e[1])
        #compute rated stories
        story_ratings=[ (story,sum(current[w] for w in story_words \
                        if w not in already_seen and current[w]>=SIGNIFICANCE_CONSTANT))\
                for story,story_words in ((s,tokenize(s)) for s in stories)]
        story_ratings.sort(key=lambda e:e[1])

    for k,(t,dummy) in already_seen.items(): #If a keyword hasn't been seen in a month, it's interesting again
        if now-t>86400*60:
                del already_seen[k]
    if cur:
        print "The latest popular words are:"
        for word in cur:
            print "%s (%d)" % word
            already_seen[word[0]]=now,word[1] #Only update already_seen at the end
    print "The most popular stories are:"
    for s,rating in story_ratings:
        if rating>0:
            print "%s (%d)"%(s,rating)
    f=open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb")
    cPickle.dump((already_seen),f,-1)
    f.close()
    f=open(os.path.expanduser("~/.popurls.pck"),"wb")
    cPickle.dump((time_fetched,story_ratings,cur),f,-1)
    f.close()
    f=open(os.path.expanduser("~/.popurls_alreadyseen_links.pck"),"wb")
    cPickle.dump(already_seen_links,f,-1)
    f.close()

def show_popular_words():
    import cPickle
    import os
    common=set(unicode(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"common.txt")).read(),"utf8").split(","))
    a=cPickle.load(open(os.path.expanduser("~/.popurls_alreadyseen.pck"))).items()
    a.sort(key=lambda e:e[1][1])
    for k in a:
        if k[0] not in common and len(k[0])>1 and k[1][1]>1: print "%s (%d)"%(k[0],k[1][1])

if __name__=='__main__':
    from sys import argv,exit
    import getopt
    optlist, args = getopt.getopt(argv[1:], '',['popular']) 

    #user values                                                            
    for o, a in optlist:
        if o == "--popular":
            show_popular_words()
            sys.exit()
    
    show_original_stuff()
