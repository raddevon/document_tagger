import re
import sys
from pg_sample_texts import DIV_COMM, MAG_CART
 
documents = [DIV_COMM, MAG_CART]

# first we need to do something with the user supplied keywords
# which we're getting with sys.argv. Remember, the script name itself
# is at index 0 in sys.argv, so we'll slice everything from index 1 forward.
searches = {}
for kw in sys.argv[1:]:
  searches[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)

for i, doc in enumerate(documents):
  print "***" * 25
  print "Here's the keyword info for doc {}:".format(i)
  for search in searches:
    print "\"{0}\": {1}".format(search, len(re.findall(searches[search], doc)))
