# kindle2evernote2

Export Kindle's My Clippings.txt to Evernote.

My original script is available at the [kindle2evernote](https://github.com/benhorvath/kindle2evernote) repo. This script was based on scraping a single page from Amazon containing all of a user's Kindle highlights.

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


## Get Started

### Dependencies

The main dependencies are the HTML parsing library [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) and the [Evernote API Python SDK](https://github.com/evernote/evernote-sdk-python).

BeautifulSoup can be installed by:

    pip install BeautifulSoup4

The Evernote SDK requires:

    git submodule add git://github.com/evernote/evernote-sdk-python/ evernote
    git submodule init
    git submodule update

Then go the installed directoy and run setup.py:

    python setup.py install

### Evernote Developer Token

You'll need an Evernote Developer token. Go to [https://www.evernote.com/api/DeveloperToken.action](https://www.evernote.com/api/DeveloperToken.action) to get a developer token for you **production** account. Mine looks like: S=aDD:U=DDDDDD:E=15SDFSDFDF:C=35234234:A=en-devtoken:V=2:H=SDFKJSDKFJKSDJFKSDJFKJSD. Note that this is not the Evernote API secret.

Save the key in a text file. You will input this file's path as a required argument to Kindle2Evernote.py.

### Get Your Highlights

Access your Kindle Highlights via My Clippings.txt file in every Kindle, and save it locally.

The path to this local file is a required argument to Kindle2Evernote.py.

### Run the Script

Open a terminal window and run:

    python kindle2evernote.py `My Clippings.txt` en_auth.txt

If you wish to specify a specific notebook to add the highlights to, use the -n or --notebook option:

    python kindle2evernote.py `My Clippings.txt` en_auth.txt -n Books

To see log output, use the -v or --verbose option

    python kindle2evernote.py `My Clippings.txt` en_auth.txt -v

## About

This project began as a fork of [**mattnorris's WhisperNote**](https://github.com/mattnorris/whispernote). By the time I was finished with my modifications, however, it was almost a completely new code base. The only remaining similarities between WhisperNote and Kindle2Evernote are the formatting of the notes in Evernote themselves. Perhaps the greatest difference is Whispernote used Gmail to load the notes to Evernote, while my script completely relies on the Evernote API -- and now also uses My Highlights.txt (since Amazon revamped their Kinde notes page.) My script also makes heavy use of object oriented paradigmn which is not that case for Whispernote.

### TODO
The base functionality of the project has been completed, but I have several changes in mind for the cuture. See TODO.txt. The biggest change I envision is for Kindle2Evernote to remember what notes it's already added.

## Contact

Please contact me at benhorvath@gmail.com if you encounter any unhandled errors preventing a smooth user experience.
