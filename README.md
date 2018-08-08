# kindle2evernote2

Export Kindle's My Clippings.txt to Evernote.

My original script is available at the [kindle2evernote](https://github.com/benhorvath/kindle2evernote) repo. This script was based on scraping a single page from Amazon
containing all of a user's Kindle highlights.

Sometime in 2018, Amazon changed this interface and the original strategy was
no longer an option.

This is an attempt to use My Clippings.txt rather than read.kindle.com. I hope
to add a number of additional features as well.

TODO
====
- Process My Clippings.txt into discrete data
- Test new clippings in the original EverNote API object
- Algorithm to convert highlights into a short ID code
- Keep store of note IDs already processed
- Write script to run process upon mounting Kindle for Mac OS
