#!/usr/bin/env python3
# -*- coding: utf-8 -*-

txt = open('My Clippings.txt', 'r').read()

clips = txt.split("""\n==========\n""")

for clip in clips:
    delimited = clip.replace("""\n\n""", '|')
    k = delimited.split('|')
    for i in k:
    	print(i)
    	print('\n')  # 0 is title, author, location
    	             # 1 is date added
    	             # 2 is highlight text
    print('\n')

    # Make sure to delete "you have reached your highlight limit"