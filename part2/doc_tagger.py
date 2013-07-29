import re
import sys
import os
from pg_sample_texts import DIV_COMM, MAG_CART

directory = sys.argv[1] | os.getcwd()
documents = os.listdir(directory)

# PREPARE OUR REGEXES FOR METADATA SEARCHES #
title_search = re.compile(
    r'(?:title:\s*)(?P<title>([\s\S](?!\n.+:))*)', re.IGNORECASE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(
    r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(
    r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)
doc_body_search = re.compile(
    r'(\*{3}\s*START.*\n+)(?P<body>(.*\n)*?)(\s*(?:\*{3}\s*)+END)')

# Find and output meta tags
for i, doc in enumerate(documents):
    title = re.search(title_search, doc).group('title')
    author = re.search(author_search, doc)
    translator = re.search(translator_search, doc)
    illustrator = re.search(illustrator_search, doc)
    if author:
        author = author.group('author')
    if translator:
        translator = translator.group('translator')
    if illustrator:
        illustrator = illustrator.group('illustrator')
    print "***" * 25
    print "Here's the info for doc {}:".format(i)
    print "Title:  {}".format(title)
    print "Author(s): {}".format(author)
    print "Translator(s): {}".format(translator)
    print "Illustrator(s): {}".format(illustrator)
    print "\n"

# Keyword Search ################
searches = {}
keywords = sys.argv[1:]
if keywords:
    for kw in keywords:
        searches[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)
    for i, doc in enumerate(documents):
        print re.search(doc_body_search, doc)
        print "***" * 25
        print "Here's the keyword info for doc {}:".format(i)
        doc_body = re.search(doc_body_search, doc).group('body')
        print re.search(doc_body_search, doc).group('body')
        for search in searches:
            print "\"{0}\": {1}".format(search, len(re.findall(searches[search], doc_body)))
