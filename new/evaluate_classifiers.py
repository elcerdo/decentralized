#!/usr/bin/env python
import utils
from datamodel import *

def test_classifiers():
    import classifiers
    import database as db
    s=db.Session()
    links=s.query(Link).filter(Link.evaluation != None).all()
    results={}
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        print "- "+cl_name+":";current.print_self()
        results[cl_name]=0
        for l in links:
            if current.predict(l) == l.evaluation:
                results[cl_name]+=1
    for k in results.keys():
        results[k]=float(results[k])/len(links)
    return results

if __name__ == '__main__':
    results=test_classifiers()
    for method in results.keys():
        print method,":",results[method]
    s=db.Session()
    links=s.query(Link).filter(Link.evaluation != None).all()
    print "Global accuracy:",float(sum(1-abs(l.combined_prediction - l.evaluation)\
        for l in links)) / len(links)
