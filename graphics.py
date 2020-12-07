'''Make drawing, animating, and creating games as easy as using Turtle.'''

# This module is designed to be a thin layer on top of tkinter that
# makes drawing, animating, and creating games as easy as using the
# Turtle module.  The use of the module is to help in learning Python
# and programming and as a result has several design decisions that
# make it less useful for creating practical graphical programs.
# These decisions include:

# 1. Requires Python 3.

# 2. Does not require any external libraries or modules.

# 3. Can not add GUI elements.

# 4. Only supports 1 window.

# 5. No object instantiation required.

# 6. No callback functions required.

# As a result of these design decisions the module can not do the
# following:

# 1. Re-size Images.  Tkinter can only re-size images using the Python
# Imaging Library which is an external library that requires Python 2.

# 2. Full-screen - Undecorated windows in Python 3 can not get focus
# and can not get keyboard input.

# 3. Sound - There is no cross-platform, built-in support for playing
# sound in Python.

# 4. Open Images Other Than GIF (And PPM) - Tkinter can only open other
# images types using the Python Imaging Library.

# 5. Multiple Windows - Without object instantiation adding windows
# would be clunky.

# See the test code at the bottom of this file for an example of how
# to use this module.

import tkinter
import time
from os import system
from platform import system as platform

# Initial window width in pixels, can be changed in code, but not by user.
INITIAL_WIDTH = 640

# Initial window height in pixels, can be changed in code, but not by user.
INITIAL_HEIGHT = 480

# Initial window title text.
INITIAL_TITLE = ""

# Initial background color of the window, any Tkinter color string can be used.
INITIAL_BACKGROUND_COLOR = "white"

# Font name for all drawn text, any Tkinter font name can be used.
TEXT_FONT = "Helvetica"

class _Graphics:
    '''Class that represents a simple graphical window.

    The class is meant to be private so that object instantiation is
    not needed by the user and so that only one window is created.

    '''
    def __init__(self):
        '''Initialize a Tkinter window.

        The window will be filled with a canvas and with mouse and
        keyboard handlers.  The window will not be displayed until one
        of the global draw functions is called so that the initial
        state of the window can be changed before display.

        '''

        # Initialize attributes
        self.running = True
        self.images = {}
        self.keys_down = {}
        self.keys_pressed = []
        self.keys_released = []
        self.buttons_down = {}
        self.buttons_pressed = []
        self.buttons_released = []
        self.return_typed = False
        self.mouse_moved = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.previous_time = time.clock()
        # self.after_idle_id = None
        self.after_idle_ids = {}

        # Initialize window
        self.window = tkinter.Tk()
        self.window.resizable(0, 0)
        self.window.protocol("WM_DELETE_WINDOW", self.handle_window_close)
        self.window.title(INITIAL_TITLE)
        self.frame = tkinter.Frame(self.window)
        self.frame.focus_set()
        self.frame.bind("<Escape>", self.handle_window_close)
        self.frame.bind("<Key>", self.handle_key_press)
        self.frame.bind("<KeyRelease>", self.handle_key_release)
        self.window.bind("<Button>", self.handle_mouse_press)
        self.window.bind("<ButtonRelease>", self.handle_mouse_release)
        self.window.bind("<Motion>", self.handle_mouse_motion)
        self.window.bind("<Enter>", self.handle_mouse_motion)
        self.frame.pack()
        self.canvas = tkinter.Canvas(self.frame)
        self.canvas.config(width=INITIAL_WIDTH, height=INITIAL_HEIGHT)
        self.canvas.config(background=INITIAL_BACKGROUND_COLOR)
        self.canvas.config(borderwidth=0)
        self.canvas.config(highlightthickness=0)
        self.canvas.pack()
        if platform() == 'Darwin':
            system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def handle_window_close(self, event=None):
        '''Handle user closing the window.

        Handle window close by updating the running state so that
        redraw only occurs if the window is open.

        '''
        self.running = False

    def handle_mouse_press(self, event):
        '''Handle mouse button press.

        Handle mouse button press, including the scroll wheel, by
        updating the mouse button state dictionary.

        '''
        self.buttons_down[event.num] = True
        self.buttons_pressed.append(event.num)

    def handle_mouse_release(self, event):
        '''Handle mouse button release.

        Handle mouse button release, including the scroll wheel, by
        updating the mouse button state dictionary.

        '''
        self.buttons_down[event.num] = False
        self.buttons_released.append(event.num)

    def handle_mouse_motion(self, event):
        '''Handle mouse movement.

        Handle mouse movement by updating the mouse movement state.

        '''
        self.mouse_moved = True
        self.mouse_x = event.x
        self.mouse_y = event.y

    def handle_key_press(self, event):
        '''Handle keyboard key press.

        If the event queue is empty, handle keyboard key press by
        updating the keyboard key state dictionary.  If the event
        queue is not empty, clear pending key release event.  See
        :func:`~graphics._Graphics.handle_after_idle` for a for more
        information.

        '''
        after_idle_id = self.after_idle_ids.get(event.keysym, None)
        if after_idle_id != None:
            self.window.after_cancel(after_idle_id)
            self.after_idle_ids[event.keysym] = None
        else:
            self.keys_down[event.keysym] = True
            self.keys_pressed.append(event.keysym)

    def handle_key_release(self, event):
        '''Handle keyboard key release.

        Schedule handling a keyboard key release when the event queue
        is empty.  See :func:`~graphics._Graphics.handle_after_idle`
        for a for more information.

        '''
        after_idle_id = self.window.after_idle(self.handle_after_idle, event)
        self.after_idle_ids[event.keysym] = after_idle_id

    def handle_after_idle(self, event):
        '''Handle after idle event.

        On OS X and Linux holding down a keyboard key uses the
        operating system key repeat, which causes repeated
        key down/key up events.  To ignore the up-down events while the
        key is pressed, key released events are not handled
        immediately.  Instead they are handled after the event queue
        is empty, by using the tkinter after_idle event.  If a
        subsequent key down event occurs before the event queue is
        emptied the release is ignored.  If no subsequent key down
        event occurs the key release is handled.  Note this causes a
        slight delay in the handling of key release events.  This
        solution is from `this
        <http://www.daniweb.com/software-development/python/threads/70746/keypress-event-with-holding-down-the-key>`_
        article.

        '''
        self.after_idle_ids[event.keysym] = None
        self.keys_down[event.keysym] = False
        self.keys_released.append(event.keysym)

    def handle_return(self, event):
        self.return_typed = True
        self.frame.focus_set()

def image_size(image_name):
    '''Return the size of the specified image when drawn to the Graphics window.

    :param str image_name: The file name of the image to draw.

    :return: (int, int) -- The width and height of the image as a tuple
        of integers.

    If ``image_name`` is not a valid image file (0, 0) is returned.

    '''
    if image_name not in graphics.images:
        try:
            image = tkinter.PhotoImage(file=image_name)
        except:
            print('ERROR: Could not load the file "{}".'.format(image_name))
            image = None
        graphics.images[image_name] = image
    else:
        image = graphics.images[image_name]
    if image is not None:
        return (image.width(), image.height())
    else:
        return (0, 0)

def image_width(image_name):
    '''Return the width of the specified image when drawn to the Graphics window.

    :param str image_name: The file name of the image to draw.

    :return: int -- The width of the image as an integer.

    If ``image_name`` is not a valid image file 0 is returned.

    '''
    image_width, image_height = image_size(image_name)
    return image_width;

def image_height(image_name):
    '''Return the height of the specified image when drawn to the Graphics window.

    :param str image_name: The file name of the image to draw.

    :return: int -- The height of the image as an integer.

    If ``image_name`` is not a valid image file 0 is returned.

    '''
    image_height, image_height = image_size(image_name)
    return image_height;

def draw_image(image_name, x, y):
    '''Draw the specified image to the Graphics window.

    :param str image_name: The file name of the image to draw.  The
        image must be a GIF file.

    :param float x: The x-coordinate, in pixels, of the center of the
        image to draw.

    :param float y: The y-coordinate, in pixels, of the center of the
        image to draw.

    See :ref:`coordinate-system-label` for a description of the
    Graphics window coordinate system.

    '''
    if image_name not in graphics.images:
        try:
            image = tkinter.PhotoImage(file=image_name)
        except:
            print('ERROR: Could not load the file "{}".'.format(image_name))
            image = None
        graphics.images[image_name] = image
    else:
        image = graphics.images[image_name]
    if image is not None:
        graphics.canvas.create_image((x, y), image=image)

def draw_oval(x, y, width, height, outline="black", fill="", thickness=1):
    '''Draw the specified axis-aligned oval the Graphics window.

    :param float x: The x-coordinate, in pixels, of the center of the
        oval to draw.

    :param float y: The y-coordinate, in pixels, of the center of the
        oval to draw.

    :param float width: The width, in pixels, of the oval to draw.

    :param float height: The height, in pixels, of the oval to draw.

    :param str outline: The outline color of the oval to draw.
        Default value is 'black'.

    :param str fill: The fill color of the oval to draw.  Default
        value is an empty string, do not fill.

    :param float thickness: The thickness, in pixels, of the outline of
        the oval to draw.  Default value is 1.

    See :ref:`coordinate-system-label` for a description of the
    Graphics window coordinate system.

    '''
    left = x - width / 2
    top = y - height / 2
    right = x + width / 2
    bottom = y + height / 2
    graphics.canvas.create_oval(left, top, right, bottom,
                                outline=outline, fill=fill, width=thickness)

def draw_rectangle(x, y, width, height, outline="black", fill="",
                   thickness=1):
    '''Draw the specified axis-aligned rectangle the Graphics window.

    :param float x: The x-coordinate, in pixels, of the center of the
        rectangle to draw.

    :param float y: The y-coordinate, in pixels, of the center of the
        rectangle to draw.

    :param float width: The width, in pixels, of the rectangle to draw.

    :param float height: The height, in pixels, of the rectangle to draw.

    :param str outline: The outline color of the rectangle to draw.
        Default value is 'black'.

    :param str fill: The fill color of the rectangle to draw.  Default
        value is an empty string, do not fill.

    :param float thickness: The thickness, in pixels, of the outline of
        the rectangle to draw.  Default value is 1.

    See :ref:`coordinate-system-label` for a description of the
    Graphics window coordinate system.

    '''
    left = x - width / 2
    top = y - height / 2
    right = x + width / 2
    bottom = y + height / 2
    graphics.canvas.create_rectangle(left, top, right, bottom,
                                outline=outline, fill=fill, width=thickness)

def draw_line(x1, y1, x2, y2, fill="black", thickness=1):
    '''Draw the specified line the Graphics window.

    :param float x1: The x-coordinate, in pixels, of first endpoint of
        the line to draw.

    :param float y1: The y-coordinate, in pixels, of the frist
        endpoint of the line to draw.

    :param float x2: The x-coordinate, in pixels, of second endpoint of
        the line to draw.

    :param float y2: The y-coordinate, in pixels, of the second
        endpoint of the line to draw.

    :param str fill: The color of the line to draw.  Default value is
        black.

    :param float thickness: The thickness, in pixels, of the line to
        draw.  Default value is 1.

    See :ref:`coordinate-system-label` for a description of the
    Graphics window coordinate system.

    '''
    graphics.canvas.create_line(x1, y1, x2, y2, fill=fill, width=thickness)

def draw_sprite(sprite):
    '''Draw the specified sprite to the Graphics window.

    :param Sprite sprite: The sprite object to draw.

    '''
    draw_image(sprite.image_name, sprite.x, sprite.y)

def text_size(text, size=12):
    '''Return the size of the specified text when drawn to the Graphics window.

    :param str text: The text to get the size of.

    :param int size: The size, in points, of the text to get the size of.

    :return: (int, int) -- The width and height of the text as a tuple
        of integers.

    '''
    temp_canvas = tkinter.Canvas()
    text_id = temp_canvas.create_text((0, 0), text=text, font=(TEXT_FONT, size))
    left, top, right, bottom = temp_canvas.bbox(text_id)
    width = right - left
    height = bottom - top
    temp_canvas.destroy()
    return (width, height)

def draw_text(text, x, y, color="black", size=12):
    '''Draw the specified text to the Graphics window.

    :param str text: The text to draw to the window.

    :param float x: The x-coordinate, in pixels, of the center of the
        text to draw.

    :param float y: The y-coordinate, in pixels, of the center of the
        text to draw.

    :param str color: The color of the text to draw.  Default value is
        'black'.

    :param int size: The size, in points, of the text to draw.
        Default value is 12.

    See :ref:`coordinate-system-label` for a description of the
    Graphics window coordinate system.

    See :ref:`colors-label` for a description of valid TKinter color
    strings.

    '''
    graphics.canvas.create_text((x, y), text=text, fill=color,
                                font=(TEXT_FONT, size))

def clear():
    '''Clear all images, shapes, and text drawn to the Graphics window.

    '''
    graphics.canvas.delete(tkinter.ALL)

def wait(seconds=0.033333333):
    '''Waits for the specified number of seconds.

    Images and text are drawn to a non-visible image buffer when the
    draw functions are called so that multiple draw calls can be
    displayed at once using this function.  This makes for smoother,
    better looking animation.  This function also blocks until the
    time specified has elapsed since the last time this function was
    called.  This allows the user to create animations at a constant
    frame rate by calling this function once for every frame of
    animation.

    Note, this is a blocking function.  When invoked, the calling program
    will stop until the user releases a mouse button.

    '''
    graphics.keys_pressed = []
    graphics.keys_released = []
    graphics.buttons_pressed = []
    graphics.buttons_released = []
    graphics.mouse_moved = False
    graphics.window.update()
    current_time = time.clock()
    elapsed_time = current_time - graphics.previous_time
    if elapsed_time < seconds:
        sleep_time = seconds - elapsed_time
        elapsed_time = sleep_time
        time.sleep(sleep_time)
    graphics.previous_time = current_time
    return elapsed_time

def mainloop():
    '''Keep the Graphics window open.

    This function is to be used to keep the program from ending when
    no animation is being done, aka displaying a drawing.  This will
    keep the Graphics window open until the user closes the window,
    either by hitting the escape key or by clicking on the window
    close button, or until ``window_open(False)`` is called.

    For example::
        >>> draw_something_brilliant()  # you must supply this function
        >>> mainloop() # window will stay open

    '''
    while graphics.running:
        wait()

def window_size(width=None, height=None):
    '''Return or set size of the Graphics window.

    :param int width: The width of the window drawing area, in pixels.

    :param int height: The height of the window drawing area, in pixels.

    :return: (int, int) -- The current width and height of the window
        as a tuple of integers.

    For example::
        >>> graphics.window_size(640, 480)  # the drawing area will be 640 x 480
        >>> print(graphics.window_size())
        >>> (640, 480)
        >>> graphics.window_size(width=480) # the drawing area width will be 480
        >>> print(graphics.window_size())
        >>> (480, 480)

    '''
    canvas_width = int(graphics.canvas.cget("width"))
    canvas_height = int(graphics.canvas.cget("height"))
    if width is None and height is None:
        return (canvas_width, canvas_height)
    if width is not None:
        canvas_width = width
    if height is not None:
        canvas_height = height
    graphics.canvas.config(width=canvas_width)
    graphics.canvas.config(height=canvas_height)
    graphics.canvas.pack()
    return (canvas_width, canvas_height)

def window_width(width=None):
    '''Return or set width of the Graphics window.

    :param int width: The width of the window drawing area, in pixels.

    :return: int -- The current width of the window as an integer.

    For example::
        >>> graphics.window_width(640)  # the drawing area will be 640px wide
        >>> print(graphics.window_width())
        >>> 640
        >>> graphics.window_size(480) # the drawing area will be 480px wide
        >>> print(graphics.window_width())
        >>> 480

    '''
    canvas_width, canvas_height = window_size(width=width, height=None)
    return canvas_width;

def window_height(height=None):
    '''Return or set height of the Graphics window.

    :param int height: The height of the window drawing area, in pixels.

    :return: int -- The current height of the window as an integer.

    For example::
        >>> graphics.window_height(480)  # the drawing area will be 640px wide
        >>> print(graphics.window_height())
        >>> 480
        >>> graphics.window_size(640) # the drawing area will be 480px wide
        >>> print(graphics.window_height())
        >>> 640

    '''
    canvas_width, canvas_height = window_size(width=None, height=height)
    return canvas_height

def window_title(title=None):
    '''Return or set the title of the Graphics window.

    :param str title: The title of the Graphics window.

    :return: (str) -- The current window title.

    For example::
        >>> graphics.window_title('Mine')  # window title will be 'Mine'
        >>> print(graphics.window_title())
        >>> Mine
        >>> graphics.window_title('Not Yours')  # window title will be 'Not Yours'
        >>> print(graphics.window_title())
        >>> Not Yours

    '''
    if title is None:
        return graphics.window.title()
    graphics.window.title(title)

def window_background_color(color=None):
    '''Return or set the background color of the Graphics window.

    :param str color: The color to set the background of the
        window to.

    :return: (str) -- The current window background color.

    See :ref:`colors-label` for a description of valid TKinter color
        strings.

    For example::
        >>> graphics.window_background_color('black')  # black window background
        >>> print(graphics.window_background_color())
        >>> black
        >>> graphics.window_background_color('white')  # white window background
        >>> print(graphics.window_background_color())
        >>> white

    '''
    if color is None:
        return graphics.canvas.cget("background")
    graphics.canvas.config(background=color)

def window_open(win_open=None):
    '''Return or set  whether the Graphics window is open.

    :param bool win_open: Whether to open or close the window.

    :return: (bool) -- Whether the window is open or closed.

    For example::
        >>> graphics.window_open(True)  # The window will open if it isn't already
        >>> print(graphics.window_open())
        >>> True
        >>> graphics.window_open(False) # The window will close if it isn't already
        >>> print(graphics.window_open())
        >>> False

    '''
    if win_open is None:
        return graphics.running
    graphics.running = win_open

def key_down(key_symbol):
    '''Return whether the specified keyboard key is currently down.

    :param str button_symbol: A valid TKinter key symbol string.

    :return: (bool) -- True if the specified keyboard key is
        being pressed, false otherwise.

    See :ref:`key-symbols-label` for a list of valid key symbols.

    '''
    return graphics.keys_down.get(key_symbol, False)

def key_up(key_symbol):
    '''Return whether the specified keyboard key is currently up.

    :param str button_symbol: A valid TKinter key symbol string.

    :return: (bool) -- True if the specified keyboard key is not
        being pressed, false otherwise.

    See :ref:`key-symbols-label` for a list of valid key symbols.

    '''
    return not graphics.keys_down.get(key_symbol, False)

def key_pressed(key_symbol):
    '''Return whether the specified keyboard key was pressed.

    :param str key_symbol: A valid TKinter key symbol string.

    :return: (bool) -- True if the specified keyboard key was
        pressed, false otherwise.

    See :ref:`key-symbols-label` for a list of valid key symbols.

    Note, this function returns whether the specified key was pressed
    since the last time the wait function was called.  It is
    meant to be used in a program with an active loop that calls the
    wait function every iteration.

    '''
    return key_symbol in graphics.keys_pressed

def key_released(key_symbol):
    '''Return whether the specified keyboard key was released.

    :param str key_symbol: A valid TKinter key symbol string.

    :return: (bool) -- True if the specified keyboard key was
        released, false otherwise.

    See :ref:`key-symbols-label` for a list of valid key symbols.

    Note, this function returns whether the specified key was released
    since the last time the wait function was called.  It is
    meant to be used in a program with an active loop that calls the
    wait function every iteration.

    '''
    return key_symbol in graphics.keys_released

def wait_for_key_press():
    '''Waits for the user to press a key and returns the key symbol.

    :return: (str) -- The TKinter key symbol string of the key pressed
        by the user.

    See :ref:`key-symbols-label` for a list of key symbols.

    Note, this is a blocking function.  When invoked, the calling program
    will stop until the user presses a keyboard key.

    '''
    while not graphics.keys_pressed:
        wait()
    key_pressed = graphics.keys_pressed.pop(0)
    return key_pressed

def wait_for_key_release():
    '''Waits for the user to release a key and returns the key symbol.

    :return: (str) -- The TKinter key symbol string of the key released
        by the user.

    See :ref:`key-symbols-label` for a list of key symbols.

    Note, this is a blocking function.  When invoked, the calling program
    will stop until the user releases a keyboard key.

    '''
    while not graphics.keys_released:
        wait()
    key_released = graphics.keys_released.pop(0)
    return key_released

def wait_for_text(x, y, foreground='black', background='white',
                  size=12, width=20):
    '''Waits for the user to type text into text box and returns text

    :param float x: The x-coordinate, in pixels, of the center of the
        text box.

    :param float y: The y-coordinate, in pixels, of the center of the
        text box.

    :param str foreground: The color of the text in the text box.
        Default value is 'black'.

    :param str background: The color of the background of the text
        box.  Default value is 'white'.

    :param int size: The font size, in points, of the text in the text
        box.  Default value is 12.

    :param int width: The width, in characters, of the text box.
        Default value is 20.

    :return: (str) -- The text entered by the user.

    Note, this is a blocking function.  When invoked, the calling program
    will stop until the user presses the return key.

    '''
    entry = tkinter.Entry(graphics.window, bg=background, fg=foreground,
                          borderwidth=size/12, font=(TEXT_FONT, size),
                          highlightthickness=0, width=width)
    entry.bind('<KeyRelease-Return>', graphics.handle_return)
    entry_window = graphics.canvas.create_window(x, y, window=entry)
    entry.focus_set()
    while not graphics.return_typed:
        wait()
    graphics.return_typed = False
    entered_text = entry.get()
    entry.destroy()
    return entered_text

def button_down(button_number):
    '''Return whether the specified mouse button is currently down.

    :param int button_number: A valid TKinter button number.

    :return: (bool) -- True if the specified mouse button is
        being pressed, false otherwise.

    See :ref:`button-numbers-label` for a list of valid button numbers.

    '''
    return graphics.buttons_down.get(button_number, False)

def button_up(button_number):
    '''Return whether the specified mouse button is currently up.

    :param int button_number: A valid TKinter button number.

    :return: (bool) -- True if the specified mouse button is not
        being pressed, false otherwise.

    See :ref:`button-numbers-label` for a list of valid button numbers.

    '''
    return not graphics.buttons_down.get(button_number, False)

def button_pressed(button_number):
    '''Return whether the specified mouse button was pressed.

    :param int button_number: A valid TKinter button number.

    :return: (bool) -- True if the specified mouse button was
        pressed, false otherwise.

    See :ref:`button-numbers-label` for a list of valid button numbers.

    Note, this function returns whether the specified button was
    pressed since the last time the wait function was called.
    It is meant to be used in a program with an active loop that calls
    the wait function every iteration.

    '''
    return button_number in graphics.buttons_pressed

def button_released(button_number):
    '''Return whether the specified mouse button was released.

    :param int button_number: A valid TKinter button number.

    :return: (bool) -- True if the specified mouse button was
        released, false otherwise.

    See :ref:`button-numbers-label` for a list of valid button numbers.

    Note, this function returns whether the specified button was
    released since the last time the wait function was called.  It is
    meant to be used in a program with an active loop that calls the
    wait function every iteration.

    '''
    return button_number in graphics.buttons_released

def wait_for_button_press():
    '''Waits for the user to press a mouse button and returns the number.

    :return: (int) -- The TKinter mouse button number of the mouse
        button pressed by the user.

    See :ref:`button-numbers-label` for a list of button numbers.

    Note, this is a blocking function.  When invoked, the calling program
    will stop until the user presses a mouse button.

    '''
    while not graphics.buttons_pressed:
        wait()
    button_pressed = graphics.buttons_pressed.pop(0)
    return button_pressed

def wait_for_button_release():
    '''Waits for the user to release a mouse button and returns the number.

    :return: (int) -- The TKinter mouse button number of the mouse
        button released by the user.

    See :ref:`button-numbers-label` for a list of button numbers.

    Note, this is a blocking function.  When invoked, the calling program
    will stop until the user releases a mouse button.

    '''
    while not graphics.buttons_released:
        wait()
    button_released = graphics.buttons_released.pop(0)
    return button_released

def mouse_x():
    '''Return the x coordinate of the mouse's current location.'''
    return graphics.mouse_x

def mouse_y():
    '''Return the y coordinate of the mouse's current location.'''
    return graphics.mouse_y

def mouse_moved():
    '''Return whether the mouse moved.

    Note, this function returns whether the mouse moved since the last
    time the wait function was called.  It is meant to be used in a
    program with an active loop that calls the wait function every
    iteration.

    '''
    return graphics.mouse_moved

graphics = _Graphics()

# If this module is run, display a simple example of text bouncing
# around the screen
if __name__ == "__main__":
    # initialize sprite variables
    sprite_text = "testing..."
    sprite_color = "black"
    sprite_size = 48
    window_width, window_height = window_size()
    sprite_width, sprite_height = text_size(sprite_text, sprite_size)
    sprite_half_width = sprite_width / 2
    sprite_half_height = sprite_height / 2
    sprite_x = (window_width + sprite_width) / 2
    sprite_y = (window_height + sprite_height) / 2
    sprite_delta_x = 6
    sprite_delta_y = 4

    # animate
    while window_open():
        # clear window
        clear()

        # update sprite location and velocity
        sprite_x += sprite_delta_x
        sprite_y += sprite_delta_y
        sprite_left = sprite_x - sprite_half_width
        sprite_right = sprite_x + sprite_half_width
        sprite_top = sprite_y - sprite_half_height
        sprite_bottom = sprite_y + sprite_half_height
        if sprite_left < 0 and sprite_delta_x < 0:
            sprite_delta_x *= -1
        elif sprite_right > window_width and sprite_delta_x > 0:
            sprite_delta_x *= -1
        elif sprite_top < 0 and sprite_delta_y < 0:
            sprite_delta_y *= -1
        elif sprite_bottom > window_height and sprite_delta_y > 0:
            sprite_delta_y *= -1

        # draw the updated sprite
        draw_text(sprite_text, sprite_x, sprite_y, sprite_color, sprite_size)

        # wait to slow the animation to 30 frames per second
        wait()
