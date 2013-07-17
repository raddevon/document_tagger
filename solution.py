import re, sys
from pg_sample_texts import DIV_COMM, MAG_CART

documents = [DIV_COMM, MAG_CART]

# PREPARE OUR REGEXES FOR METADATA SEARCHES #
# we'll use re.compile() here, which allows you to assign a regex pattern
# to a variable. We'll do this for each our metadata fields.
#
# Also note how we're using paretheses to create two search groups. Looking
# at title_search, see how we use one group to match on the presence of "title:".
#
# Also, note how in the second group is a named group -- we use ?p<name> .
#
# Finally, note that we're passing the re.IGNORECASE flag as an optional
# argument to re.compile. We're doing this because it's human beings who create
# the metadata headers at the top of Project gutenberg docs, and we want to account
# for possibility of "title: Some Title", "Title: Some Title", and "TITLE: Some Title").

# Breakdown of title regex:
# (?:title:\s*)- grab the word 'title' followed by a colon and any number of space
# characters. The '?:' insures this group is not captured.
# (?P<title>- Capture a group named 'title'
# [\s\S]- get any space or non-space character
# (?!\n.+:)- not followed by a newline, one or more non-newline characters, and a colon
# *- and grab zero or more of these characters.
title_search = re.compile(r'(?:title:\s*)(?P<title>([\s\S](?!\n.+:))*)', re.IGNORECASE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)

# now iterate over the documents and extract and print output about metadata
# for each one. Note the use of enumerate here, which gives you a counter variable
# (in this case 'i') that keeps track of the index of the list (in this case documents)
# your currently on in your loop. You should memorize how enumerate works, and google it
# if you need more explanation. It's a highly productive built in function, and there are
# common problems that you'll encounter as a programmer that enumerate is great for.
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

################ Keyword Search ################
# first we need to do something with the user supplied keywords
# which we're getting with sys.argv. Remember, the script name itself
# is at index 0 in sys.argv, so we'll slice everything from index 1 forward.
searches = {}
keywords = sys.argv[1:]
if keywords:
  for kw in keywords:
    searches[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)

  for i, doc in enumerate(documents):
    print "***" * 25
    print "Here's the keyword info for doc {}:".format(i)
    for search in searches:
      print "\"{0}\": {1}".format(search, len(re.findall(searches[search], doc)))