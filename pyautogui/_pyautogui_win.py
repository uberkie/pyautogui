# Windows implementation of PyAutoGUI functions.
# BSD license
# Al Sweigart al@inventwithpython.com

import ctypes
import ctypes.wintypes
import pyautogui
from pyautogui import LEFT, MIDDLE, RIGHT

import sys
if sys.platform !=  'win32':
    raise Exception('The pyautogui_win module should only be loaded on a Windows system.')


# Fixes the scaling issues where PyAutoGUI was reporting the wrong resolution:
try:
   ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass # Windows XP doesn't support this, so just do nothing.


"""
A lot of this code is probably repeated from win32 extensions module, but I didn't want to have that dependency.

Note: According to http://msdn.microsoft.com/en-us/library/windows/desktop/ms646260(v=vs.85).aspx
the ctypes.windll.user32.mouse_event() function has been superseded by SendInput.

SendInput() is documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646310(v=vs.85).aspx

UPDATE: SendInput() doesn't seem to be working for me. I've switched back to mouse_event()."""


# Event codes to be passed to the mouse_event() win32 function.
# Documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646273(v=vs.85).aspx
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_RIGHTCLICK = MOUSEEVENTF_RIGHTDOWN + MOUSEEVENTF_RIGHTUP
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MIDDLECLICK = MOUSEEVENTF_MIDDLEDOWN + MOUSEEVENTF_MIDDLEUP

MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x01000

# Documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646304(v=vs.85).aspx
KEYEVENTF_KEYDOWN = 0x0000 # Technically this constant doesn't exist in the MS documentation. It's the lack of KEYEVENTF_KEYUP that means pressing the key down.
KEYEVENTF_KEYUP = 0x0002

# Documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646270(v=vs.85).aspx
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', ctypes.wintypes.LONG),
        ('dy', ctypes.wintypes.LONG),
        ('mouseData', ctypes.wintypes.DWORD),
        ('dwFlags', ctypes.wintypes.DWORD),
        ('time', ctypes.wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', ctypes.wintypes.WORD),
        ('wScan', ctypes.wintypes.WORD),
        ('dwFlags', ctypes.wintypes.DWORD),
        ('time', ctypes.wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', ctypes.wintypes.DWORD),
        ('wParamL', ctypes.wintypes.WORD),
        ('wParamH', ctypes.wintypes.DWORD)
    ]

class INPUT(ctypes.Structure):
    class _I(ctypes.Union):
        _fields_ = [
            ('mi', MOUSEINPUT),
            ('ki', KEYBDINPUT),
            ('hi', HARDWAREINPUT),
        ]

    _anonymous_ = ('i', )
    _fields_ = [
        ('type', ctypes.wintypes.DWORD),
        ('i', _I),
    ]
# End of the SendInput win32 data structures.



""" Keyboard key mapping for pyautogui:
Documented at http://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx

The *KB dictionaries in pyautogui map a string that can be passed to keyDown(),
keyUp(), or press() into the code used for the OS-specific keyboard function.

They should always be lowercase, and the same keys should be used across all OSes."""
keyboardMapping = dict([(key, None) for key in pyautogui.KEY_NAMES]) | {
    'backspace': 0x08,  # VK_BACK
    '\b': 0x08,  # VK_BACK
    'super': 0x5B,  # VK_LWIN
    'tab': 0x09,  # VK_TAB
    '\t': 0x09,  # VK_TAB
    'clear': 0x0C,  # VK_CLEAR
    'enter': 0x0D,  # VK_RETURN
    '\n': 0x0D,  # VK_RETURN
    'return': 0x0D,  # VK_RETURN
    'shift': 0x10,  # VK_SHIFT
    'ctrl': 0x11,  # VK_CONTROL
    'alt': 0x12,  # VK_MENU
    'pause': 0x13,  # VK_PAUSE
    'capslock': 0x14,  # VK_CAPITAL
    'kana': 0x15,  # VK_KANA
    'hanguel': 0x15,  # VK_HANGUEL
    'hangul': 0x15,  # VK_HANGUL
    'junja': 0x17,  # VK_JUNJA
    'final': 0x18,  # VK_FINAL
    'hanja': 0x19,  # VK_HANJA
    'kanji': 0x19,  # VK_KANJI
    'esc': 0x1B,  # VK_ESCAPE
    'escape': 0x1B,  # VK_ESCAPE
    'convert': 0x1C,  # VK_CONVERT
    'nonconvert': 0x1D,  # VK_NONCONVERT
    'accept': 0x1E,  # VK_ACCEPT
    'modechange': 0x1F,  # VK_MODECHANGE
    ' ': 0x20,  # VK_SPACE
    'space': 0x20,  # VK_SPACE
    'pgup': 0x21,  # VK_PRIOR
    'pgdn': 0x22,  # VK_NEXT
    'pageup': 0x21,  # VK_PRIOR
    'pagedown': 0x22,  # VK_NEXT
    'end': 0x23,  # VK_END
    'home': 0x24,  # VK_HOME
    'left': 0x25,  # VK_LEFT
    'up': 0x26,  # VK_UP
    'right': 0x27,  # VK_RIGHT
    'down': 0x28,  # VK_DOWN
    'select': 0x29,  # VK_SELECT
    'print': 0x2A,  # VK_PRINT
    'execute': 0x2B,  # VK_EXECUTE
    'prtsc': 0x2C,  # VK_SNAPSHOT
    'prtscr': 0x2C,  # VK_SNAPSHOT
    'prntscrn': 0x2C,  # VK_SNAPSHOT
    'printscreen': 0x2C,  # VK_SNAPSHOT
    'insert': 0x2D,  # VK_INSERT
    'del': 0x2E,  # VK_DELETE
    'delete': 0x2E,  # VK_DELETE
    'help': 0x2F,  # VK_HELP
    'win': 0x5B,  # VK_LWIN
    'winleft': 0x5B,  # VK_LWIN
    'winright': 0x5C,  # VK_RWIN
    'apps': 0x5D,  # VK_APPS
    'sleep': 0x5F,  # VK_SLEEP
    'num0': 0x60,  # VK_NUMPAD0
    'num1': 0x61,  # VK_NUMPAD1
    'num2': 0x62,  # VK_NUMPAD2
    'num3': 0x63,  # VK_NUMPAD3
    'num4': 0x64,  # VK_NUMPAD4
    'num5': 0x65,  # VK_NUMPAD5
    'num6': 0x66,  # VK_NUMPAD6
    'num7': 0x67,  # VK_NUMPAD7
    'num8': 0x68,  # VK_NUMPAD8
    'num9': 0x69,  # VK_NUMPAD9
    'multiply': 0x6A,  # VK_MULTIPLY  ??? Is this the numpad *?
    'add': 0x6B,  # VK_ADD  ??? Is this the numpad +?
    'separator': 0x6C,  # VK_SEPARATOR  ??? Is this the numpad enter?
    'subtract': 0x6D,  # VK_SUBTRACT  ??? Is this the numpad -?
    'decimal': 0x6E,  # VK_DECIMAL
    'divide': 0x6F,  # VK_DIVIDE
    'f1': 0x70,  # VK_F1
    'f2': 0x71,  # VK_F2
    'f3': 0x72,  # VK_F3
    'f4': 0x73,  # VK_F4
    'f5': 0x74,  # VK_F5
    'f6': 0x75,  # VK_F6
    'f7': 0x76,  # VK_F7
    'f8': 0x77,  # VK_F8
    'f9': 0x78,  # VK_F9
    'f10': 0x79,  # VK_F10
    'f11': 0x7A,  # VK_F11
    'f12': 0x7B,  # VK_F12
    'f13': 0x7C,  # VK_F13
    'f14': 0x7D,  # VK_F14
    'f15': 0x7E,  # VK_F15
    'f16': 0x7F,  # VK_F16
    'f17': 0x80,  # VK_F17
    'f18': 0x81,  # VK_F18
    'f19': 0x82,  # VK_F19
    'f20': 0x83,  # VK_F20
    'f21': 0x84,  # VK_F21
    'f22': 0x85,  # VK_F22
    'f23': 0x86,  # VK_F23
    'f24': 0x87,  # VK_F24
    'numlock': 0x90,  # VK_NUMLOCK
    'scrolllock': 0x91,  # VK_SCROLL
    'shiftleft': 0xA0,  # VK_LSHIFT
    'shiftright': 0xA1,  # VK_RSHIFT
    'ctrlleft': 0xA2,  # VK_LCONTROL
    'ctrlright': 0xA3,  # VK_RCONTROL
    'altleft': 0xA4,  # VK_LMENU
    'altright': 0xA5,  # VK_RMENU
    'browserback': 0xA6,  # VK_BROWSER_BACK
    'browserforward': 0xA7,  # VK_BROWSER_FORWARD
    'browserrefresh': 0xA8,  # VK_BROWSER_REFRESH
    'browserstop': 0xA9,  # VK_BROWSER_STOP
    'browsersearch': 0xAA,  # VK_BROWSER_SEARCH
    'browserfavorites': 0xAB,  # VK_BROWSER_FAVORITES
    'browserhome': 0xAC,  # VK_BROWSER_HOME
    'volumemute': 0xAD,  # VK_VOLUME_MUTE
    'volumedown': 0xAE,  # VK_VOLUME_DOWN
    'volumeup': 0xAF,  # VK_VOLUME_UP
    'nexttrack': 0xB0,  # VK_MEDIA_NEXT_TRACK
    'prevtrack': 0xB1,  # VK_MEDIA_PREV_TRACK
    'stop': 0xB2,  # VK_MEDIA_STOP
    'playpause': 0xB3,  # VK_MEDIA_PLAY_PAUSE
    'launchmail': 0xB4,  # VK_LAUNCH_MAIL
    'launchmediaselect': 0xB5,  # VK_LAUNCH_MEDIA_SELECT
    'launchapp1': 0xB6,  # VK_LAUNCH_APP1
    'launchapp2': 0xB7,  # VK_LAUNCH_APP2
}
# Populate the basic printable ascii characters.
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
for c in range(32, 128):
    keyboardMapping[chr(c)] = ctypes.windll.user32.VkKeyScanA(ctypes.wintypes.WCHAR(chr(c)))


def _keyDown(key):
    """Performs a keyboard key press without the release. This will put that
    key in a held down state.

    NOTE: For some reason, this does not seem to cause key repeats like would
    happen if a keyboard key was held down on a text field.

    Args:
      key (str): The key to be pressed down. The valid names are listed in
      pyautogui.KEY_NAMES.

    Returns:
      None
    """
    if key not in keyboardMapping or keyboardMapping[key] is None:
        return

    needsShift = pyautogui.isShiftCharacter(key)

    """
    # OLD CODE: The new code relies on having all keys be loaded in keyboardMapping from the start.
    if key in keyboardMapping.keys():
        vkCode = keyboardMapping[key]
    elif len(key) == 1:
        # note: I could use this case to update keyboardMapping to cache the VkKeyScan results, but I've decided not to just to make any possible bugs easier to reproduce.
        vkCode = ctypes.windll.user32.VkKeyScanW(ctypes.wintypes.WCHAR(key))
        if vkCode == -1:
            raise ValueError('There is no VK code for key "%s"' % (key))
        if vkCode > 0x100: # the vk code will be > 0x100 if it needs shift
            vkCode -= 0x100
            needsShift = True
    """
    mods, vkCode = divmod(keyboardMapping[key], 0x100)

    for apply_mod, vk_mod in [(mods & 4, 0x12), (mods & 2, 0x11),
        (mods & 1 or needsShift, 0x10)]: #HANKAKU not supported! mods & 8
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYDOWN, 0) #
    ctypes.windll.user32.keybd_event(vkCode, 0, KEYEVENTF_KEYDOWN, 0)
    for apply_mod, vk_mod in [(mods & 1 or needsShift, 0x10), (mods & 2, 0x11),
        (mods & 4, 0x12)]: #HANKAKU not supported! mods & 8
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0) #


def _keyUp(key):
    """Performs a keyboard key release (without the press down beforehand).

    Args:
      key (str): The key to be released up. The valid names are listed in
      pyautogui.KEY_NAMES.

    Returns:
      None
    """
    if key not in keyboardMapping or keyboardMapping[key] is None:
        return

    needsShift = pyautogui.isShiftCharacter(key)
    """
    # OLD CODE: The new code relies on having all keys be loaded in keyboardMapping from the start.
    if key in keyboardMapping.keys():
        vkCode = keyboardMapping[key]
    elif len(key) == 1:
        # note: I could use this case to update keyboardMapping to cache the VkKeyScan results, but I've decided not to just to make any possible bugs easier to reproduce.
        vkCode = ctypes.windll.user32.VkKeyScanW(ctypes.wintypes.WCHAR(key))
        if vkCode == -1:
            raise ValueError('There is no VK code for key "%s"' % (key))
        if vkCode > 0x100: # the vk code will be > 0x100 if it needs shift
            vkCode -= 0x100
            needsShift = True
    """
    mods, vkCode = divmod(keyboardMapping[key], 0x100)

    for apply_mod, vk_mod in [(mods & 4, 0x12), (mods & 2, 0x11),
        (mods & 1 or needsShift, 0x10)]: #HANKAKU not supported! mods & 8
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, 0, 0) #
    ctypes.windll.user32.keybd_event(vkCode, 0, KEYEVENTF_KEYUP, 0)
    for apply_mod, vk_mod in [(mods & 1 or needsShift, 0x10), (mods & 2, 0x11),
        (mods & 4, 0x12)]: #HANKAKU not supported! mods & 8
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0) #


def _position():
    """Returns the current xy coordinates of the mouse cursor as a two-integer
    tuple by calling the GetCursorPos() win32 function.

    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.
    """

    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)


def _size():
    """Returns the width and height of the screen as a two-integer tuple.

    Returns:
      (width, height) tuple of the screen size, in pixels.
    """
    return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))


def _moveTo(x, y):
    """Send the mouse move event to Windows by calling SetCursorPos() win32
    function.

    Args:
      button (str): The mouse button, either 'left', 'middle', or 'right'
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.

    Returns:
      None
    """
    ctypes.windll.user32.SetCursorPos(x, y)
    # This was a possible solution to issue #314 https://github.com/asweigart/pyautogui/issues/314
    # but I'd like to hang on to SetCursorPos because mouse_event() has been superseded.
    #_sendMouseEvent(MOUSEEVENTF_MOVE + MOUSEEVENTF_ABSOLUTE, x, y)


def _mouseDown(x, y, button):
    """Send the mouse down event to Windows by calling the mouse_event() win32
    function.

    Args:
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.
      button (str): The mouse button, either 'left', 'middle', or 'right'

    Returns:
      None
    """
    if button not in (LEFT, MIDDLE, RIGHT):
        raise ValueError(
            f'button arg to _click() must be one of "left", "middle", or "right", not {button}'
        )

    if button == LEFT:
        EV = MOUSEEVENTF_LEFTDOWN
    elif button == MIDDLE:
        EV = MOUSEEVENTF_MIDDLEDOWN
    elif button == RIGHT:
        EV = MOUSEEVENTF_RIGHTDOWN

    try:
        _sendMouseEvent(EV, x, y)
    except OSError:
        # TODO: We need to figure out how to prevent these errors, see https://github.com/asweigart/pyautogui/issues/60
        pass


def _mouseUp(x, y, button):
    """Send the mouse up event to Windows by calling the mouse_event() win32
    function.

    Args:
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.
      button (str): The mouse button, either 'left', 'middle', or 'right'

    Returns:
      None
    """
    if button not in (LEFT, MIDDLE, RIGHT):
        raise ValueError(
            f'button arg to _click() must be one of "left", "middle", or "right", not {button}'
        )

    if button == LEFT:
        EV = MOUSEEVENTF_LEFTUP
    elif button == MIDDLE:
        EV = MOUSEEVENTF_MIDDLEUP
    elif button == RIGHT:
        EV = MOUSEEVENTF_RIGHTUP

    try:
        _sendMouseEvent(EV, x, y)
    except OSError:
        pass


def _click(x, y, button):
    """Send the mouse click event to Windows by calling the mouse_event() win32
    function.

    Args:
      button (str): The mouse button, either 'left', 'middle', or 'right'
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.

    Returns:
      None
    """
    if button not in (LEFT, MIDDLE, RIGHT):
        raise ValueError(
            f'button arg to _click() must be one of "left", "middle", or "right", not {button}'
        )

    if button == LEFT:
        EV = MOUSEEVENTF_LEFTCLICK
    elif button == MIDDLE:
        EV = MOUSEEVENTF_MIDDLECLICK
    elif button ==RIGHT:
        EV = MOUSEEVENTF_RIGHTCLICK

    try:
        _sendMouseEvent(EV, x, y)
    except OSError:
        # TODO: We need to figure out how to prevent these errors, see https://github.com/asweigart/pyautogui/issues/60
        pass


def _sendMouseEvent(ev, x, y, dwData=0):
    """The helper function that actually makes the call to the mouse_event()
    win32 function.

    Args:
      ev (int): The win32 code for the mouse event. Use one of the MOUSEEVENTF_*
      constants for this argument.
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.
      dwData (int): The argument for mouse_event()'s dwData parameter. So far
        this is only used by mouse scrolling.

    Returns:
      None
    """
    assert x != None and y != None, 'x and y cannot be set to None'
    # TODO: ARG! For some reason, SendInput isn't working for mouse events. I'm switching to using the older mouse_event win32 function.
    #mouseStruct = MOUSEINPUT()
    #mouseStruct.dx = x
    #mouseStruct.dy = y
    #mouseStruct.mouseData = ev
    #mouseStruct.time = 0
    #mouseStruct.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0)) # according to https://stackoverflow.com/questions/13564851/generate-keyboard-events I can just set this. I don't really care about this value.
    #inputStruct = INPUT()
    #inputStruct.mi = mouseStruct
    #inputStruct.type = INPUT_MOUSE
    #ctypes.windll.user32.SendInput(1, ctypes.pointer(inputStruct), ctypes.sizeof(inputStruct))

    # TODO Note: We need to handle additional buttons, which I believe is documented here:
    # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event

    width, height = _size()
    convertedX = 65536 * x // width + 1
    convertedY = 65536 * y // height + 1
    ctypes.windll.user32.mouse_event(ev, ctypes.c_long(convertedX), ctypes.c_long(convertedY), dwData, 0)

    # TODO: Too many false positives with this code: See: https://github.com/asweigart/pyautogui/issues/108
    #if ctypes.windll.kernel32.GetLastError() != 0:
    #    raise ctypes.WinError()


def _scroll(clicks, x=None, y=None):
    """Send the mouse vertical scroll event to Windows by calling the
    mouse_event() win32 function.

    Args:
      clicks (int): The amount of scrolling to do. A positive value is the mouse
      wheel moving forward (scrolling up), a negative value is backwards (down).
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.

    Returns:
      None
    """
    startx, starty = _position()
    width, height = _size()

    if x is None:
        x = startx
    elif x < 0:
        x = 0
    elif x >= width:
        x = width - 1
    if y is None:
        y = starty
    elif y < 0:
        y = 0
    elif y >= height:
        y = height - 1

    try:
        _sendMouseEvent(MOUSEEVENTF_WHEEL, x, y, dwData=clicks)
    except OSError:
        pass


def _hscroll(clicks, x, y):
    """Send the mouse horizontal scroll event to Windows by calling the
    mouse_event() win32 function.

    Args:
      clicks (int): The amount of scrolling to do. A positive value is the mouse
      wheel moving right, a negative value is moving left.
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.

    Returns:
      None
    """
    return _scroll(clicks, x, y)


def _vscroll(clicks, x, y):
    """A wrapper for _scroll(), which does vertical scrolling.

    Args:
      clicks (int): The amount of scrolling to do. A positive value is the mouse
      wheel moving forward (scrolling up), a negative value is backwards (down).
      x (int): The x position of the mouse event.
      y (int): The y position of the mouse event.

    Returns:
      None
    """
    return _scroll(clicks, x, y)

