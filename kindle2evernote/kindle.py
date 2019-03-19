#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Object for parsing and accessing Kindle notes from My Clippings.txt."""

from datetime import datetime
import json
import logging
import os

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
        clips = clippings_txt.strip().split("""\r\n==========\r\n""")
        highlights = []
        for i, clip in enumerate(clips):
            if 'Highlight on page' in clip:
                delimited = clip.replace("""\r\n\r\n""", ' | ').replace('\r\n-', ' | ')
                split = delimited.split(' | ')
                title_author = split[0].replace('(', ' | ').replace(')', '').split(' | ')
                title, author = title_author[0].strip(), title_author[1].strip()
                loc = split[1].replace(' Your Highlight on', '').strip() + ', ' + split[2]
                date_added = datetime.strptime(split[3], 'Added on %A, %B %d, %Y %X %p')
                clip_text = split[4].replace('==========', '').strip()
                clip_id = loc.replace('Location ', '').replace('-', '') + date_added.strftime('%Y%m%d%H%M%S')
            elif 'You have reached the clipping limit' in clip:
                continue
            else:
                delimited = clip.replace("""\r\n\r\n""", ' | ').replace('\r\n-', ' | ')
                split = delimited.split(' | ')
                title_author = split[0].replace('(', ' | ').replace(')', '').strip()
                title, author = title_author.split(' | ')
                loc = split[1].replace('Your Highlight on ', '').strip()
                date_added = datetime.strptime(split[2], 'Added on %A, %B %d, %Y %X %p')
                clip_text = split[3].replace('==========', '').strip()
                clip_id = loc.replace('Location ', '').replace('-', '') + date_added.strftime('%Y%m%d%H%M%S')

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


class KindleHighlightsIndex(object):
    """ Stores a simple Python dictionary with highlight ID and date of upload to
    Evernote."""

    def __init__(self, path):
        self.path = path
        self.archive = self.__read(path)

    def __read(self, path):
        if not os.path.exists(path):
            index = dict()
        else:
            with open(path, 'r+') as index_file:    
                index = json.load(index_file)
        return index

    def contains(self, clip_id):
        if clip_id in self.archive.keys():
            return True
        else:
            return False

    def update(self, highlight, write=True):
        if not self.contains(highlight['clip_id']):
            self.archive[highlight['clip_id']] = highlight['date_added']
            if write == True:
                self.write()

    def write(self):
        with open(self.path, 'w+') as index_file:
            json.dump(self.archive, index_file)

    def delete(self, clip_id, write=True):
        del self.archive[clip_id]
        if write == True:
            self.write()

    def __repr__(self):
        return str(self.archive)

    def __getitem__(self, i):
        return self.archive[i]

    def __iter__(self):
        for clip in self.archive:
            yield clip

    def __len__(self):
        return len(self.archive)
