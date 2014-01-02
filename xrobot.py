#!/usr/bin/env python

from __future__ import print_function # python2

import Xlib.display
import Xlib.XK
import Xlib.ext.xtest
import numpy as np

try:
    import gtk.gdk
    _GTK_AVAILABLE = True
except ImportError:
    import sys
    message = 'WARNING: Could not load gtk.gdk. Screen capture will be slow.\n'
    sys.stderr.write(message)
    _GTK_AVAILABLE = False

class XRobot(object):
    """
    XRobot captures the screen, simulates keyboard presses, mouse movements 
    and clicks under the X11 window system.
    """
    def __init__(self):
        """
        Build and returns object, as expected.
        """
        self.display = Xlib.display.Display()
        # If the line above prints 'Xlib.protocol.request.QueryExtension' and it
        # bothers you, check:
        # http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=566172
        self.screen = self.display.screen()
        self.root = self.screen.root

        self.size = (self.screen['width_in_pixels'], 
                     self.screen['height_in_pixels'])

        if not _GTK_AVAILABLE:
            self.capture_screen = self._capture_screen_xlib

    def screen_resolution(self):
        """ 
        Returns (width, height) of the screen at the time of creation of 
        the XRobot object.
        """
        return self.size

    def click(self, button):
        """ Press and release mouse 'button'
        (1:left, 2:middle, 3:right, 4:scroll up 5: scroll down). """
        self.mouse_down(button)
        self.mouse_up(button)

    def mouse_down(self, button):
        """ Press mouse 'button' 
        (1:left, 2:middle, 3:right, 4:scroll up 5: scroll down). """
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.ButtonPress, button)
        self.display.sync()

    def mouse_up(self, button):
        """ Release mouse 'button'
        (1:left, 2:middle, 3:right, 4:scroll up 5: scroll down). """
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.ButtonRelease, button)
        self.display.sync()

    def move(self, x, y):
        """ Move mouse pointer to (x, y) coordinates. """
        self.root.warp_pointer(x, y)
        self.display.sync()

    def mouse_pos(self):
        """ Returns (x, y) mouse pointer coordinates. """
        mouse_data = self.root.query_pointer()._data
        return mouse_data['root_x'], mouse_data['root_y']

    def key(self, c):
        """ Press and release key associated to key description 'c'. 
        Common keys descriptions are:

        BackSpace Tab Return Escape space exclam quotedbl numbersign dollar
        ampersand quoteright parenleft parenright asterisk plus comma minus 
        period slash 0 1 2 3 4 5 6 7 8 9 colon semicolon less equal greater 
        question at bracketleft backslash bracketright asciicircum grave
        underscore a b c d e f g h i j k l m n o p q r s t u v w x y z
        Delete Up Down Right Left Insert Home End PageUp PageDown F1 F2 F3 
        F4 F5 F6 F7 F8 F9 F10 F11 F12 F13 F14 F15 Num_Lock Caps_Lock 
        Scroll_Lock Shift_R Shift_L Control_R Control_L Alt_R Alt_L

        Bear in mind that you need to press the necessary modifiers to
        generate the correct keystrokes. For instance, in order to generate
        the hash symbol ('#') you will have to: 
            xr.key_down('Shift_L')
            xr.key_down('numbersign')
            xr.key_up('numbersign')
            xr.key_up('Shift_L')
        """

        self.key_down(c)
        self.key_up(c)

    def key_down(self, c):
        """ Press key associated to key description 'c'. 
            Refer to XRobot.key docstring for common key descriptions."""
        k = self._character_to_keycode(c)
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyPress, k)
        self.display.sync()

    def key_up(self, c):
        """ Release key associated to key description 'c'.
            Refer to XRobot.key docstring for common key descriptions."""
        k = self._character_to_keycode(c)
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyRelease, k)
        self.display.sync()

    def _character_to_keycode(self, c):
        """ Find keysym associated to 'c'. """
        return self.display.keysym_to_keycode(Xlib.XK.string_to_keysym(c))

    def capture_screen(self, x=0, y=0, width=None, height=None):
        """
        Returns a copy of the screen contents as a numpy array width 
        dtype='uint8' and dimensions: (height, width, color), where 
        color is ordered as (R, G, B).
        If you find odd that height goes first, please refer to:
        http://docs.scipy.org/doc/numpy/reference/internals.html#multidimensional-array-indexing-order-issues
        """
        if width == None: width = self.size[0]
        if height == None: height = self.size[1]
        # From: http://ubuntuforums.org/showpost.php?p=2681009&postcount=5
        w = gtk.gdk.get_default_root_window()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
        pb = pb.get_from_drawable(w, w.get_colormap(), 0, 0, 0, 0, 
                                  width, height)
        return pb.get_pixels_array()

    def _capture_screen_xlib(self, x=0, y=0, width=None, height=None):
        """
        Fallback routine to capture the screen. Does not depend on python-gtk
        being present, but is noticeable slower than its GTK counterpart.
        """
        if width == None: width = self.size[0]
        if height == None: height = self.size[1]

        img = self.root.get_image(x, y, width, height, Xlib.X.ZPixmap, 
                                  0xffffffff)
        d = np.fromstring(img.data, dtype='uint8')
        d = d.reshape(height, width, 4)[..., :3]

        d2 = np.ndarray(d.shape, dtype='uint8')
        d2[..., 0], d2[..., 1], d2[..., 2]  = d[..., 2], d[..., 1], d[..., 0]

        return d2

if __name__ == '__main__':
    robot = XRobot()
    x, y = robot.mouse_pos()
    print('Current mouse position: x =', x, 'y =', y)
    robot.move(10, 10)
    robot.click(1)
    robot.key_down('a')
    robot.key_up('a')
    robot.key_down('comma')
    robot.key_up('comma')

    width, height = robot.screen_resolution()
    print('Screen width:', width, 'Screen height:', height)
    img = robot.capture_screen()
    import pylab as pl
    pl.imshow(img)
    pl.show()
