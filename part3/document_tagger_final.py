import re
import argparse
import os


def get_args():
    """
    Creates the parser and parses arguments passed in
    """
    parser = argparse.ArgumentParser(
        description='Extract meta data and count keywords in Project Gutenberg text.')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='The path of the directory containing files to be parsed.')
    parser.add_argument('-k', '--keyword', action='append',
                        help='Documents will be searched for these keywords.', dest='keywords')
    return parser.parse_args()


def build_kw_regex(keywords):
    """
    Takes a list of keywords.
    Returns a dictionary with compiled regular expressions keyed with search keywords.
    """
    searches = {}
    for kw in keywords:
        searches[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)
    return searches


def count_keywords(keywords, contents):
    """
    Takes a list of keywords and the contents of a Project Gutenberg text file.
    Returns a dictionary of counts keyed to their respective keywords.
    """
    searches = build_kw_regex(keywords)
    count = {}
    doc_body_search = re.compile(
        r'(\*{3}\s*START.*\n+)(?P<body>(.*\n)*?)(\s*(?:\*{3}\s*)+END)')
    doc_body = re.search(doc_body_search, contents).group('body')
    for search in searches:
        count[search] = len(re.findall(searches[search], doc_body))
    return count


def get_meta(contents):
    """
    Takes the contents of a Project Gutenberg text file.
    Returns a dictionary of meta attributes.
    """
    title_search = re.compile(
        r'(?:title:\s*)(?P<title>([\s\S](?!\n.+:))*)', re.IGNORECASE)
    author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
    translator_search = re.compile(
        r'(translator:)(?P<translator>.*)', re.IGNORECASE)
    illustrator_search = re.compile(
        r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)

    meta = {}

    meta['title'] = re.search(title_search, contents).group('title')
    author = re.search(author_search, contents)
    translator = re.search(translator_search, contents)
    illustrator = re.search(illustrator_search, contents)
    meta['author'] = author.group('author') if author else None
    meta['translator'] = translator.group('translator') if translator else None
    meta['illustrator'] = illustrator.group(
        'illustrator') if illustrator else None

    return meta


def search_files(directory, keywords=None):
    """
    Takes a directory path and optional list of keywords.
    Prints the meta information and number of instances of each keyword for each document in the directory.
    """
    files = [name for name in os.listdir(directory) if name.endswith('.txt')]
    for i, doc_file in enumerate(files):
        with open(os.path.join(directory, doc_file), 'r') as doc:
            contents = doc.read()
            meta = get_meta(contents)
            print "***" * 25
            print "Here's the info for doc {}:".format(i)
            print "Title:  {}".format(meta['title'])
            print "Author(s): {}".format(meta['author'])
            print "Translator(s): {}".format(meta['translator'])
            print "Illustrator(s): {}".format(meta['illustrator'])
            if keywords:
                print "***" * 25
                print "Here's the keyword info for doc {}:".format(i)
                kw_count = count_keywords(keywords, contents)
                for kw in kw_count:
                    print "\"{0}\": {1}".format(kw, kw_count[kw])
                print "\n"


def main():
    args = get_args()
    directory = args.directory
    keywords = args.keywords

    search_files(directory, keywords)

if __name__ == '__main__':
    main()
