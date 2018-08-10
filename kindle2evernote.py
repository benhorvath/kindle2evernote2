#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Special case with two locations:

clips[2]
Out[56]: '\ufeffMarx, Capital, and the Madness of Economic Reason (Harvey, David)\n- Your Highlight on page 138 | Location 2325-2326 | Added on Sunday, May 27, 2018 6:13:25 PM\n\nWithin all this diversity, one conceptualisation of space and time – such as clock-time and cadastral Euclidean space – may come to dominate in daily economic life.'
"""

from datetime import datetime

txt = open('My Clippings.txt', 'r').read().strip()

clips = txt.split("""\n==========\n""")

for i, clip in enumerate(clips):

    if 'Highlight on page' in clip:
        delimited = clip.replace("""\n\n""", '|').replace('\n-', '|')
        k = delimited.split('|')
        first = k[0].replace('(', '|').replace(')', '|')
        first_split = first.split('|')
        title = first_split[0].strip()
        author = first_split[1].strip()
        loc = k[1].strip() + ', ' + k[2].strip()
        loc = loc.replace('Your Highlight on', '').lower().strip()
        date_added = k[3].replace('Added on ', '').strip()
        date_added = datetime.strptime(date_added, '%A, %B %d, %Y %X %p')
    elif 'You have reached the clipping limit' in clip:
        print('CONTINUE\n\n')
        continue
    else:
        delimited = clip.replace("""\n\n""", '|')
        k = delimited.split('|')
        first = k[0].replace('(', '|').replace(')', '|')
        first_split = first.split('|')
        title = first_split[0].strip()
        author = first_split[1].strip()
        loc = first_split[2].strip()
        loc = loc.replace("""- Your Highlight on Location""", '').strip()
        # also need to replace '- Your Note on Location 348'
        date_added = k[1].replace('Added on ', '').strip()
        date_added = datetime.strptime(date_added, '%A, %B %d, %Y %X %p')

    #clipping_id = date_added.strftime('%Y%m%d%H%M%s')
    #print('ID: %s') % clipping_id
    print('Title: %s' % title)
    print('Author: %s' % author)
    print('Loc: %s' % loc)
    print('Date added: %s' % str(date_added.date()))
    print('Highlight: %s' % k[2].replace('==========', ''))
    print('\n')  # 0 is title, author, location
    # 1 is date added
    # 2 is highlight text
    print('\n')

    # Make sure to delete "you have reached your highlight limit"
