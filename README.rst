xrobot
######

Python X11 event automation library

::

    Help on module xrobot:

    NAME
        xrobot

    CLASSES
        __builtin__.object
            XRobot
        
        class XRobot(__builtin__.object)
         |  XRobot captures the screen, simulates keyboard presses, mouse movements 
         |  and clicks under the X11 window system.
         |  
         |  Methods defined here:
         |  
         |  __init__(self)
         |      Build and returns object, as expected.
         |  
         |  capture_screen(self, x=0, y=0, width=None, height=None)
         |      Returns a copy of the screen contents as a numpy array width 
         |      dtype='uint8' and dimensions: (height, width, color), where 
         |      color is ordered as (R, G, B).
         |      If you find odd that height goes first, please refer to:
         |      http://docs.scipy.org/doc/numpy/reference/internals.html#multidimensional-array-indexing-order-issues
         |  
         |  key(self, c)
         |      Press and release key associated to key description 'c'. 
         |      Common keys descriptions are:
         |      
         |      BackSpace Tab Return Escape space exclam quotedbl numbersign dollar
         |      ampersand quoteright parenleft parenright asterisk plus comma minus 
         |      period slash 0 1 2 3 4 5 6 7 8 9 colon semicolon less equal greater 
         |      question at bracketleft backslash bracketright asciicircum grave
         |      underscore a b c d e f g h i j k l m n o p q r s t u v w x y z
         |      Delete Up Down Right Left Insert Home End PageUp PageDown F1 F2 F3 
         |      F4 F5 F6 F7 F8 F9 F10 F11 F12 F13 F14 F15 Num_Lock Caps_Lock 
         |      Scroll_Lock Shift_R Shift_L Control_R Control_L Alt_R Alt_L
         |      
         |      Bear in mind that you need to press the necessary modifiers to
         |      generate the correct keystrokes. For instance, in order to generate
         |      the hash symbol ('#') you will have to: 
         |          xr.key_down('Shift_L')
         |          xr.key_down('numbersign')
         |          xr.key_up('numbersign')
         |          xr.key_up('Shift_L')
         |  
         |  key_down(self, c)
         |      Press key associated to key description 'c'. 
         |      Refer to XRobot.key docstring for common key descriptions.
         |  
         |  key_up(self, c)
         |      Release key associated to key description 'c'.
         |      Refer to XRobot.key docstring for common key descriptions.
         |  
         |  mouse_click(self, button)
         |      Press and release mouse 'button'
         |      (1:left, 2:middle, 3:right, 4:scroll up 5: scroll down).
         |  
         |  mouse_down(self, button)
         |      Press mouse 'button' 
         |      (1:left, 2:middle, 3:right, 4:scroll up 5: scroll down).
         |  
         |  mouse_move(self, x, y)
         |      Move mouse pointer to (x, y) coordinates.
         |  
         |  mouse_pos(self)
         |      Returns (x, y) mouse pointer coordinates.
         |  
         |  mouse_up(self, button)
         |      Release mouse 'button'
         |      (1:left, 2:middle, 3:right, 4:scroll up 5: scroll down).
         |  
         |  screen_resolution(self)
         |      Returns (width, height) of the screen at the time of creation of 
         |      the XRobot object.
