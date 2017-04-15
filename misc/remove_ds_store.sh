#!/usr/bin/env bash

# Anytime you use the Mac file explorer to view a directory, it adds a file '.DS_Store' that saves the view
# preferences of the user.  It's a hidden file, so whatever.  Except it throws off a lot of file operations
# in this project.  Simply run this script to remove all the .DS_Store files in the data directory.

find /storage -name '.DS_Store' -type f -delete