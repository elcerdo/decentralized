#!/usr/bin/env python


def get_classifiers():
    import re
    import os
    return [module[:-3] for module in os.listdir('classifiers') if re.match('^[^_].*\.py$',module)]


if __name__ == '__main__':
    import classifiers
    for cl_name in get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        print current.predict(None)