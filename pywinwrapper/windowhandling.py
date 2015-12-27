__author__ = 'alex'

from collections import namedtuple
import win32gui
import win32con
import win32api

"""
    +-------------------------------------------------------------------------------------------------------+
    |   Win32 Documentation                                                                                 |
    +---------------------+---------------------------------------------------------------------------------+
    | Thing               | Link                                                                            |
    +=====================+=================================================================================+
    | Point               | https://msdn.microsoft.com/en-us/library/windows/desktop/dd162805(v=vs.85).aspx |
    | Point               | https://msdn.microsoft.com/en-us/library/windows/desktop/ms633558(v=vs.85).aspx |
    | GetWindow           | https://msdn.microsoft.com/en-us/library/windows/desktop/ms633515(v=vs.85).aspx |
    | ShowWindow          | https://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx |
    | setforegroundwindow | https://msdn.microsoft.com/en-us/library/windows/desktop/ms633539(v=vs.85).aspx |
    |                     |                                                                                 |
    +---------------------+---------------------------------------------------------------------------------+
"""

screenwidth = win32api.GetSystemMetrics(0)
screenheight = win32api.GetSystemMetrics(1)

dims = namedtuple("windowDimensions", ["x", "y", "width", "height"])


class Window:
    def __init__(self, hwnd, *args, **kwargs):
        self.hwnd = hwnd
        self.attribs = dict()
        self.text = win32gui.GetWindowText(self.hwnd)
        self.dims = dims(None, None, None, None)
        self.x = self.dims.x
        self.y = self.dims.y
        self.width = self.dims.width
        self.height = self.dims.height
        self.update()

    def __str__(self):
        """
        :return: Each key value pair for the attributes of the object
        :rtype: string
        """
        return "\n".join(
            ["{} : {}".format(k, v) for k, v in self.__dict__.items()]
        )

    def getText(self):
        return win32gui.GetWindowText(self.hwnd)

    def isVisible(self):
        if win32gui.IsWindowVisible(self.hwnd):
            return True
        else:
            return False

    def getDimensions(self):
        return dims(*win32gui.GetWindowRect(self.hwnd))

    def move(self,
             x: "pos of left side of screen",
             y: "pos of right side of screen",
             width: "new width of screen",
             height: "new height of screen",
             relative=False):
        win32gui.MoveWindow(self.hwnd, x, y, width, height, True)

    def minimize(self):
        win32gui.ShowWindow(self.hwnd, 6)  # SW_MINIMIZE

    def restore(self):
        win32gui.ShowWindow(self.hwnd, 9)

    def maximize(self):
        win32gui.ShowWindow(self.hwnd, 3)

    def bringtotop(self):
        win32gui.ShowWindow(self.hwnd, 5)
        win32gui.SetForegroundWindow(self.hwnd)

    def show(self, mode, activate=True):
        if mode == "hide":
            win32gui.ShowWindow(self.hwnd, 0)
        if mode == "minimized":
            if activate == False:
                win32gui.ShowWindow(self.hwnd, 8)  # SW_SHOWNA

        win32gui.ShowWindow(self.hwnd, 5)

    def showMaximized(self):
        win32gui.ShowWindow(self.hwnd, 3)

    def close(self):
        pass

    def update(self):
        # update dimensions
        tdims = self.getDimensions()
        self.dims = self.getDimensions()
        self.x, self.y = tdims.x, tdims.y
        self.height, self.width = tdims.height, tdims.width
        # update visibility
        self.visible = self.isVisible()


# -------------------------------------------------------------------


# -------------------------------------------------------------------

def get_all_window_handles():
    found = []
    tmphandler = lambda hwnd, lparam: found.append(hwnd)
    win32gui.EnumWindows(tmphandler, None)
    return found


# -------------------------------------------------------------------
def get_visible_windows():
    foundwindows = {}
    for w in get_all_window_handles():
        if win32gui.IsWindowVisible(w):
            foundwindows[w] = Window(w)
    return foundwindows


# -------------------------------------------------------------------
def get_mouse_position():
    flags, hcursor, (x, y) = win32gui.GetCursorInfo()
    return (x, y)


# -------------------------------------------------------------------
def get_hndl_under_mouse():
    return win32gui.WindowFromPoint(
        get_mouse_position()
    )


# -------------------------------------------------------------------
def get_window_under_mouse():
    return Window(get_hndl_under_mouse())


# -------------------------------------------------------------------

def is_caps_on():
    """
    +----------+----------------------+-------+
    | Key      |  Constant            | Value |
    +----------+----------------------+-------+
    | CapsLock |  win32con.VK_CAPITAL |  20   |
    +----------+------------------+---+-------+
    |           States            |           |
    +----------+--------+---------+ //  //    +--------+
    | keystate | on/off | up/down |  0 0      | return |
    +==========+========+=========+     -127  +--------+
    | 0        | off    | up      |  ======|  | (0,1)  |
    +----------+--------+---------+_mmm____mmm+--------+
    | -127     | on     | down    |--+----+---| (1,0)  |
    +----------+--------+---------+  |    |   +--------+
    | 1        | on     | up      |  |    |   | (1,1)  |
    +----------+--------+---------+--+----+---+--------+
    | -128     | off    | down    |() () () ()| (0,0)  |
    +----------+--------+---------+-----------+--------+
    """
    capskey = win32con.VK_CAPITAL
    state = win32api.GetKeyState(capskey)
    if state in (0, -128):
        capsison = 0
    else:
        capsison = 1
    if state >= 0:
        keyisup = 1
    else:
        keyisup = 0
    return (capsison, keyisup)

# -------------------------------------------------------------------
from collections import deque


class WindowGroup:
    def __init__(self):
        self.groupMembers = deque()

    def append(self, other):
        self.groupMembers.append(other)

    def __next__(self):
        # self.groupMembers.rotate(1)
        w_ = self.groupMembers.popleft()
        self.groupMembers.append(w_)
        return w_


    # from time import sleep
    # import pywintypes
    #
    # q = WindowGroup()
    # a = get_visible_windows()
    # a = [Window(x) for x in a]
    # for x in a:
    # sleep(1)
    #     print(x)
    #     # q += x
    #     q.groupMembers.append(x)
    #     print(q.groupMembers)
    #     try:
    #         next(q).bringtotop()
    #     except pywintypes.error:
    #         pass
    # temp, a = a[0], a[1:]


if __name__ == '__main__':
    pass
    # ==============================================================
    # from time import sleep
    # # while True:
    # # sleep(.01)
    # #     print(get_caps_state())
    # # windowundermouse.move(0,0,700,200)
    # testdeque = WindowGroup()
    # count = 0
    # while count < 4:
    # if is_caps_on()[1]:
    #         windowundermouse = get_window_under_mouse()
    #         testdeque += windowundermouse
    #         while True:
    #             if is_caps_on() == (0, 0):
    #                 count += 1
    #                 break
    #                 # windowundermouse.bringtotop()
    #     else:
    #         sleep(3)
    # while True:
    #     if is_caps_on() == (1, 1):
    #         next(deque).bringtotop()
    #         while True:
    #             if is_caps_on() != (1, 1):
    #                 break
    #             else:
    #                 sleep(1)
    # ==============================================================

    # visWins = get_visible_windows()
    # for k,v in visWins.items():
    #     print('-'*10)
    #     print(v)
    # for key,val in visWins.items():
    #     val.update()
    #     print("-"*100)
    #     print(
    #         "\n".join(
    #             list(
    #                 map(
    #                     lambda x: " "*10 + x,
    #                     map(
    #                         lambda x:"{}".format(
    #                           "{}".format(x),
    #                             ),
    #                          str(val).splitlines())
    #                 ))
    #             )
    #         )

    # print("{}".format(val).center(90))


#
#
# get_visible_windows()
#
#
# def apply(f, *args, **kwargs):
# return f(*args, **kwargs)
#
#
#
#
# class Window:
# pool = []  # holds defined handle objects
#
# @classmethod
#     def populateHandler(cls, hwnd, lParam):
#         print(a)
#         W = namedtuple('window', ['hwnd',
#                                   'text',
#                                   'visible',
#                                   'x1', 'y1',
#                                   'x2', 'y2'])
# print('W defined')
#         x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
#         Window.pool.append(W(hwnd,
#                              win32gui.GetWindowText(hwnd),
#                              win32gui.IsWindowVisible(hwnd),
#                              x1, y1,
#                              x2, y2))
#
#     @classmethod
#     def populateWindows(cls):
#         win32gui.EnumWindows(Window.populateHandler, None)
#
#     @classmethod
#     def get_visible_windows(cls):
#         all_handles = []
#         h = lambda hwnd, lParam: win32gui.GetWindowRect(hwnd)
#         return [win32gui.EnumWindows(h, None)]
#         return [x for x in]
#
#
# wh = Window()
# wh.populateWindows()
# #
# #
# class Window:
# import win32gui
# import win32con
# #
# pool = []  # holds defined handle objects
# #
# def populateHandler(hwnd, lParam):
# Window.pool.append()
# #
# #
# @classmethod
# def populateWindows():
# win32gui.EnumWindows(enumHandler, None)
# #
# def enumHandler(hwnd, lParam):
# text = win32gui.GetWindowText(hwnd)
# if win32gui.IsWindowVisible(hwnd):
# visible = True
# #
# if 'Stack Overflow' in win32gui.GetWindowText(hwnd):
# win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)
# #
# def __init__(self):
# self.Name = None
# self.hwnd = None
# #
# #
# def enumHandler(hwnd, lParam):
# if win32gui.IsWindowVisible(hwnd):
# if 'Stack Overflow' in win32gui.GetWindowText(hwnd):
# win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)
# #
# def moveTo(self, x1, y1, x2, y2):
# #
# #
# win32gui.EnumWindows(enumHandler, None)
