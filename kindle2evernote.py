#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" """

from datetime import datetime
import logging
import socket

from evernote.api.client import EvernoteClient
import evernote.edam.error.ttypes as Errors
import evernote.edam.type.ttypes as Types
import evernote.edam.userstore.constants as UserStoreConstants

from kindle2evernote.kindle import KindleHighlights, KindleHighlightsIndex


class EvernoteAPI(object):
    """ Connects to EvernoteAPI. Allows access to client and note_store.
    """

    def __init__(self, auth_token, index_path='index.json', notebook=None):

        self.auth_token = auth_token
        self.notebook = notebook
        self.index = KindleHighlightsIndex(index_path)
        self.client = EvernoteClient(token=self.auth_token, sandbox=False)
        self.logger = logging.getLogger('whispernote')
        self.logger.info('Initializing EverNote API')

        for i in range(1, 4):
            self.logger.info('Attempting to retrieve Note Store')
            try:
                self.note_store = self.client.get_note_store()
                self.logger.info('Note Store retrieved')
                break
            except Errors.EDAMSystemException as e:
                if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
                    self._handle_rate_limit(e)
                else:
                    raise e
                self.logger.info('Retry no. %d' % i)
                continue
            except socket.error:
                self.logger.warn('Socket error: Retrying in 1 minute')
                sleep(60)
                self.logger.info('Retry no. %d' % i)
                continue

        self.notebook_map = self.map_notebook_guids()

    def add_notes(self, highlights):
        """ For loop to convert a list of highlights to an Evernote note
        object, then adds to Evernote.
        """
        for highlight in highlights:
            self.add_note(highlight)
            sleep(2) # be nice to API
        self.logger.info('Finished adding notes')

    def add_note(self, highlight):
        """ Takes a highlight, checks if it already exists, converts to an 
        Evernote API note object, then attempts to add to Evernote.
        """

        # if highlight['id'] in archive.keys():
            # do process
        # else:
        #    self.logger.info('Note ID already exists')
        note = self.format_note(highlight)

        for i in range(1, 4):
            self.logger.info('Attempting to create note: %s' % note.title)
            try:
                self.note_store.createNote(self.auth_token, note)
                sleep(1)  # nice to API
                self.logger.info('Success')
                break
            except Errors.EDAMUserException as e:
                self.logger.warn('Unable to parse, skipping: %s' % note.title)
                continue
            except Errors.EDAMSystemException as e:
                if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
                    self._handle_rate_limit(e)
                else:
                    raise e
                self.logger.info('Retry no. %d' % i)
                continue
            except socket.error:
                self.logger.warn('Socket error: Retrying in 1 minute')
                sleep(60)
                self.logger.info('Retry no. %d' % i)
                continue

    def map_notebook_guids(self):
        """ Returns a dictionary of a Note Store's notebook names and GUIDs
        """
        notebooks_list = self.note_store.listNotebooks()
        notebooks_map = dict([(i.name, i.guid) for i in notebooks_list])
        return notebooks_map



if __name__ == '__main__':

    # txt = open('My Clippings.txt', 'r').read().strip()

    # clips = txt.split("""\r\n==========\r\n""")

auth = open('token', 'r').read().strip()

evernote = EvernoteAPI(auth, notebook='Books', index_path='../index.json')

highlights = KindleHighlights('My Clippings.txt')




