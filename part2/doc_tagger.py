import re
import argparse
import os

parser = argparse.ArgumentParser(
    description='Extract meta data and count keywords in Project Gutenberg text.')
parser.add_argument('directory', nargs='?', default=os.getcwd(),
                    help='The path of the directory containing files to be parsed.')
parser.add_argument('-k', '--keyword', action='append',
                    help='Documents will be searched for these keywords.', dest='keywords')
args = parser.parse_args()
directory = args.directory
files = [name for name in os.listdir(directory) if name.endswith('.txt')]

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
searches = {}
keywords = args.keywords
if keywords:
    for kw in keywords:
        searches[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)
for i, doc_file in enumerate(files):
    with open(os.path.join(directory, doc_file), 'r') as doc:
        contents = doc.read()
        title = re.search(title_search, contents).group('title')
        author = re.search(author_search, contents)
        translator = re.search(translator_search, contents)
        illustrator = re.search(illustrator_search, contents)
        if author:
            author = author.group('author')
        if translator:
            translator = translator.group('translator')
        if illustrator:
            illustrator = illustrator.group('illustrator')
        # Print file meta information
        print "***" * 25
        print "Here's the info for doc {}:".format(i)
        print "Title:  {}".format(title)
        print "Author(s): {}".format(author)
        print "Translator(s): {}".format(translator)
        print "Illustrator(s): {}".format(illustrator)

        # Keyword search
        if keywords:
            print "***" * 25
            print "Here's the keyword info for doc {}:".format(i)
            doc_body = re.search(doc_body_search, contents).group('body')
            for search in searches:
                print "\"{0}\": {1}".format(search, len(re.findall(searches[search], doc_body)))
            print "\n"
        else:
            print "\n"
