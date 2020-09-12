#!/usr/bin/env python3

#
# This file is a part of the NsCDE - Not so Common Desktop Environment
# Author: Hegel3DReloaded
# Licence: GPLv3
#

import os
import sys
import shutil

nscde_root = os.environ.get('NSCDE_ROOT')
if not nscde_root:
   sys.stderr.write("NSCDE_ROOT not set. Stop.\n")
   sys.exit(1)
else:
   sys.path.append(nscde_root + "/lib/python")

themegen="""
For this script to work you need to install the Python 3
Qt4 (PyQt4) modules, or Python 3 Qt5 (PyQt5) modules.
"""

try:
   from PyQt4 import QtCore, QtGui
except ImportError:
   try:
      from PyQt5 import QtCore, QtGui
   except ImportError:
      print (themegen)
      sys.exit(1)

import Globals
from Theme import Theme
from Opts import Opts
from MotifColors import readMotifColors2

helptxt="""Generate GTK2 and GTK3 theme in style of CDE/Motif
Directory 'NsCDE' will be be created as ~/.themes/NsCDE

Usage:
   themegen <palettename> ncolors gtk2 gtk3
   or
   themegen /path/to/palettefile.dp ncolors gtk2 gtk3

Arguments:
    Palette name or file path
    CDE color palettes, are located in NSCDE_ROOT/share/palettes
    or in $HOME/.NsCDE/palettes

    Number of colors: 8 or 4
    4 colors mode was called "More Colors for Applications" in Color Style Manager
    8 colors mode was called "More Colors for Desktop" in Color Style Manager

    gtk2: generate theme files for GTK2 applications

    gtk3: generate theme files for GTK3 applications

Examples:
    HP-UX Unix style:
       themegen Broica 8 gtk2 gtk3

    Sun Solaris style:
       themegen Crimson 4 gtk2 gtk3

    Custom:
       themegen Urchin 8 gtk2 gtk3

    From file which is not in system's nor user's palette directory:
       themegen /home/jdoe/pixmaps/MyNewPalette.dp 8 gtk2 gtk3
"""

if len(sys.argv)!=5:
    print (helptxt)
    sys.exit()

try: # PyQt4
    app = QtGui.QApplication(sys.argv)
except AttributeError: # using PyQt5 ...
    app = QtGui.QGuiApplication(sys.argv)

opts=Opts()

palettefile=(sys.argv[1])
opts.ncolors=int(sys.argv[2])
opts.themeGtk2=(sys.argv[3])
opts.themeGtk3=(sys.argv[4])

userhome = os.path.expanduser("~")
nscdetheme = "NsCDE"
# nscdetheme="NsCDE-" + palettefile

if os.path.exists(userhome + "/.NsCDE/palettes/" + palettefile + ".dp"):
    opts.currentpalettefile=(userhome + "/.NsCDE/palettes/" + palettefile + ".dp")
elif os.path.exists(nscde_root + "/share/palettes/" + palettefile + ".dp"):
    opts.currentpalettefile=(nscde_root + "/share/palettes/" + palettefile + ".dp")
elif os.path.exists(palettefile):
    opts.currentpalettefile=palettefile
    # nscdetheme="NsCDE-" + os.path.basename(nscdetheme.replace(".dp", ""))
else:
    print ('Palette not found: ' + palettefile)
    sys.exit()

Globals.themedir=nscde_root + "/share/config_templates/integration/gtk2_gtk3_qt"
Globals.userthemedir=os.path.join(userhome,'.themes',nscdetheme)
Globals.themesrcdir=Globals.themedir
Globals.palettedir=os.path.join(Globals.themedir,'palettes')

theme=Theme(opts)
Globals.colorshash=readMotifColors2(opts.ncolors,opts.currentpalettefile)
theme.initTheme()
theme.updateThemeNow()

