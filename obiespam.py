from urllib import urlencode
import urllib2
from HTMLParser import HTMLParser
from time import sleep

BASE_URL = 'http://www.obietalk.com/'
POSTS_URL = 'includes/actions.php?renderposts&nopagehit=true&start=%d&sortby=%s&onlyshow=%s'
COMMENTS_URL = 'includes/actions.php?rendercomments&pid=%s'
NEW_POST_URL = 'includes/actions.php?newpost'
NEW_COMMENT_URL = 'includes/actions.php?newcomment'

class DivParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = False
        self.data = []
        self.shouldDelete = False

    def handle_starttag(self, tag, attributes):
        if self.recording:
            self.recording = False
            self.shouldDelete = True
            return
        if tag != "div":
            return
        for name, value in attributes:
            if name == "class" and value == "post_content":
                self.recording = True
                break

    def handle_data(self, data):
        if self.shouldDelete:
            self.shouldDelete = False
        elif self.recording:
            cleaned = data.strip()
            if len(cleaned) > 0:
                self.data.append(cleaned)

    def handle_endtag(self, tag):
        self.recording = False

def posts_url(start=0, sortby='sortcomment', onlyshow='onlyalltime'):
    return POSTS_URL % (start, sortby, onlyshow)

def comments_url(post_id):
    return COMMENTS_URL % post_id

# Get all posts from pages start to end, where 0 is the front page.
# Returns a list of all posts.
def get_posts(start, end):
    text = []
    for i in xrange(start, end):
        text.append(get_text(posts_url(50*i)))
    return text

def get_comments(post_id):
    return get_text(comments_url(post_id))

# Returns text for a given url, rather than HTML.
def get_text(url):
    f = urllib2.urlopen(BASE_URL + url)
    parser = DivParser()
    parser.feed(f.read())
    return parser.data[0]

def post(text):
    data = urlencode({'text': text})
    urllib2.urlopen(BASE_URL + NEW_POST_URL, data)

def comment(text, post_id):
    data = urlencode({'text': text, 'pid': post_id})
    urllib2.urlopen(BASE_URL + NEW_COMMENT_URL, data)

# Spams new posts with the contents of messages, a list. If the post_id is given,
# spams comments; otherwise new posts. Waits to avoid blocking.
def spam(messages,post_id=-1, wait=60):
    for message in messages:
        if post_id > 0:
            comment(message, post_id)
        else:
            post(message)
        sleep(wait)
