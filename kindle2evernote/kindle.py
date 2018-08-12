#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Object for parsing and accessing Kindle notes from My Clippings.txt."""

from datetime import datetime
import logging
import uuid

class KindleHighlights(object):
    """ Object input is a Kindle's My Clippings.txt file.
    """

    def __init__(self, my_clippings):
        self._highlights = self._get_all_highlights(my_clippings)
        self.logger = logging.getLogger('whispernote')
        self.logger.info('Initializing Kindle Highlights')

    def _get_all_highlights(self, my_clippings):
        doc = open(my_clippings, 'r').read()
        return self._parse_highlights(doc)

    def _parse_highlights(self, clippings_txt):
        clips = clippings_txt.strip().split("""\n==========\n""")
        highlights = []
        for i, clip in enumerate(clips):
            if 'Highlight on page' in clip:
                delimited = clip.replace("""\n\n""", ' | ').replace('\n-', ' | ')
                split = delimited.split(' | ')
                title_author = split[0].replace('(', ' | ').replace(')', '').split(' | ')
                try:
                    title, author = title_author[0].strip(), title_author[1].strip()
                except:
                    print(i)
                loc = split[1].replace(' Your Highlight on', '').strip() + ', ' + split[2]
                date_added = datetime.strptime(split[3], 'Added on %A, %B %d, %Y %X %p')
                clip_text = split[4].replace('==========', '').strip()
                clip_id = str(uuid.uuid4())
            elif 'You have reached the clipping limit' in clip:
                continue
            else:
                delimited = clip.replace("""\n\n""", ' | ').replace('\n-', ' | ')
                split = delimited.split(' | ')
                title_author = split[0].replace('(', ' | ').replace(')', '').strip()
                try:
                    title, author = title_author.split(' | ')
                except:
                    print(i)
                loc = split[1].replace('Your Highlight on ', '').strip()
                date_added = datetime.strptime(split[2], 'Added on %A, %B %d, %Y %X %p')
                clip_text = split[3].replace('==========', '').strip()
                clip_id = str(uuid.uuid4())

            highlights.append({'clip_id': clip_id,
                               'title': title,
                               'author': author,
                               'loc': loc,
                               'date_added': str(date_added.date()),
                               'text': clip_text})
        return highlights

    def __getitem__(self, i):
        return self._highlights[i]

    def __iter__(self):
        for hl in self._highlights:
            yield hl

    def __len__(self):
        return len(self._highlights)