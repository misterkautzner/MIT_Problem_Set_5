# 6.00 Problem Set 5
#
# Name: John Kautzner
# Collaborators: None
# Time: 9:00
#
# RSS Feed Filter
#

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    """
    """
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        print "Trigger's evaluate"
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger

class WordTrigger(Trigger):
    def __init__(self, word):
        Trigger.__init__(self)
        self.word = word

    def is_word_in(self, text):
        thisWord = ''
        for c in text:
            if c == ' ' or c in string.punctuation:
                if(thisWord == self.word.lower()):
                    return True

                thisWord = ''

            else:
                thisWord += c.lower()
        
        return False

##def test_is_word_in():
##    t = 'Koala bears are soft and cuddly.'
##    q = 'I prefer pillows that are soft.'
##    r = 'Soft drinks are great.'
##    s = "Soft's the new pink!"
##    p = '"Soft!" he exclaimed as he threw the football.'
##    u = "Microsoft announced today that pillows are bad."
##    v = "I softly ran."
##
##    soft = WordTrigger('soft')
##
##    for i in [p, q, r, s, t, u, v]:
##        print i, "       ", soft.is_word_in(i)
##            
##    print
##    return "Completed"

    

# TODO: TitleTrigger

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
        #self.word = word

    def evaluate(self, story):
        title = story.get_title()
        return self.is_word_in(title)
        
"""
    def word_in_title():
        title = self.get_title()
        if(word.is_word_in(title):
           return word, "is in title"

        return None
"""    
    
# TODO: SubjectTrigger

class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
        #self.word = word

    def evaluate(self, story):
        subject = story.get_subject()
        return self.is_word_in(subject)

# TODO: SummaryTrigger

class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        #WordTrigger.__init__(self, word)
        self.word = word

    def evaluate(self, story):
        summary = story.get_summary()
        return self.is_word_in(summary)

# Composite Triggers    

# Problems 6-8

# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, newsItem):
        return not self.trigger.evaluate(newsItem)
        

# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def evaluate(self, newsItem):
        return self.trig1.evaluate(newsItem) and self.trig2.evaluate(newsItem)

# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def evaluate(self, newsItem):
        return self.trig1.evaluate(newsItem) or self.trig2.evaluate(newsItem)  

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        Trigger.__init__(self)
        self.phrase = phrase

    def is_phrase_in(self, text):
        if self.phrase in text:
            return True
        return False

    def evaluate(self, newsItem):
        title = newsItem.get_title()
        subject = newsItem.get_subject()
        summary = newsItem.get_summary()
        return self.is_phrase_in(title) or self.is_phrase_in(subject) or self.is_phrase_in(summary)


#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    triggeredStories = []
    
    for story in stories:
        for trigger in triggerlist:
            if(trigger.evaluate(story)):
                triggeredStories.append(story)
                break

    return triggeredStories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones

    trigs = {}
    TrigSet = []

    for l in lines:
        words = [] # List of all words in a line
        #count = 0
        name = '' # Whatever word in the line is being assembled.
        
        for char in l:
            if char != ' ':
                #count += 1
                name += char
            else:
                words += [name]
                name = ''

        if(words[0] == 'ADD'):
            for i in range(1, len(words)):
                Trigset += words[i]
                

        else:
            if(words[1] == 'TITLE'):
                trigs[words[0]] = TitleTrigger(words[2])

            elif(words[1] == 'SUBJECT'):
                trigs[words[0]] = SubjectTrigger(words[2])

            elif(words[1] == 'SUMMARY'):
                trigs[words[0]] = SummaryTrigger(words[2])

            elif(words[1] == 'NOT'):
                trigs[words[0]] = NotTrigger(words[2])

            elif(words[1] == 'AND'):
                trigs[words[0]] = AndTrigger(words[2], words[3])

            elif(words[1] == 'OR'):
                trigs[words[0]] = OrTrigger(words[2], words[3])

            elif(words[1] == 'PHRASE'):
                phrase = ''
                for word in range(2, len(words)):
                    phrase += words[word]
                    if(word != len(words)):
                        phrase += ' '

                trigs[words[0]] = PhraseTrigger(phrase)

            else:
                print "Trigger type is undefined"
                
            print "Dictating"
            
    for trigger in TrigSet:
        print "Printing Trigs"
        print trigs[trigger]
        

    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)
"""
SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

"""
