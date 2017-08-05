# Discazos

Last update: February 2013.

Django app. Developed on Django 1.4.

This is a website developed in Django, a chrome extension that interact with it and a simple-minimal flash music player (without UI).

## What may be interesting from this source code?

Probably not Django code, but JS code.

The idea es similar to the one that Cuevana site made famous: To retrive content from an external File Hosting site (like megaupload) and stream it to the user through a website. To allow this interaction, a chrome extension is needed.

The file streamed is a SINGLE mp3 file with a full album. The site player (flash + JS) would allow the user to change tracks by offsetting this file.

This album file is supposed to be generated from a physical disc using this desktop app:  https://github.com/lucianolev/discazos-creator

### Interesting source to look at

**Website side:** https://github.com/lucianolev/discazos/tree/master/discazos/albums/static/js
**Chrome extension:** https://github.com/lucianolev/discazos/tree/master/extensions/chrome/discazos-player-connector
