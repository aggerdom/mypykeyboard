__author__ = 'alex'
import mykbcodes
from win32api import GetKeyboardState, GetKeyState
from mykbcodes import Keycode2Description, Description2Keycode
import win32con
from time import sleep
# use a queue to store the keys that were pressed
# print len(mykbcodes.KEYcode2description) #len 178
# print len(mykbcodes.description2KEYcode) #len 176

class pyKeyBoard:
    # TODO
    # 1. Account for the fact that some keyboards treat the shift keys as toggles
    def __init__(self):
        self._definedkeyindices = Keycode2Description.keys()
        self._definedkeynames = Keycode2Description.values()
        pass

    def kbname(self,keyarg):
        """:keyarg:
        Description -> Keycode
        Keycode -> Description
        """
        if type(keyarg)==str:
            return Description2Keycode[keyarg]
        elif type(keyarg)==int:
            return Keycode2Description[keyarg]

    def kbcheck(self,listofkeycodes=None):
        GetKeyState(1) # Force Windows to update keyboard buffer
        keystates = bytearray(GetKeyboardState())
        if listofkeycodes != None:
            # scan a restricted list of keys
            for k in listofkeycodes:
                if keystates[k]:
                    yield k
                    #yield [k for k in listofkeycodes if keystates[k]]
        else:
            for i, state in enumerate(keystates):
                if (i in self._definedkeyindices) and (state):
                    yield i, state, keycode2num(i)



    def scanKB(self,barray=None):
        # We don't really care about the value of this call
        # Saddly it adds overhead but it is currently needed
        # to force windows to update the virtualkey buffer
        #
        # print '---'*30
        GetKeyState(1)
        barray = bytearray(GetKeyboardState())
        # barray = bytearray(barray)
        for i, state in enumerate(barray):
            if (i in mykbcodes.Keycode2Description.keys()) & state:
                # print state
                yield i, state, keycode2num(i)

"""
BOOL WINAPI GetKeyboardState(
  _Out_ PBYTE lpKeyState
);
"""



# Interesting odd case, vk()

def keycode2num(number):
    "function to get keyname from number"
    return mykbcodes.Keycode2Description[number]

GetKeyState(1)


def scanKB(barray=None):
    # We don't really care about the value of this call
    # Saddly it adds overhead but it is currently needed
    # to force windows to update the virtualkey buffer
    #
    # print '---'*30
    GetKeyState(1)
    barray = bytearray(GetKeyboardState())
    # barray = bytearray(barray)
    for i, state in enumerate(barray):
        if (i in mykbcodes.Keycode2Description.keys()) & (state):
            # print state
            yield i, state, keycode2num(i)
        #print i, state,

# found_ = set()
# a = None
# for time in range(100):
#     new_val = list(scanKB())
#     sleep(.1)
#     if a is not None:
#         for a in new_val:
#             if a not in found_:
#                 found_ = found_.add(a)
#             print a
#         # print new_val
#         print new_val

if __name__ == '__main__':
    # for foo in list(scanKB()):
    #     print foo
    #
    # last_ = []
    # for count in range(100):
    #     keys_ = [i for i in scanKB()]
    #     if keys_ != last_:
    #         print keys_
    #         last_ = keys_
    #     sleep(1)
    KB = pyKeyBoard()
    countdown = 1000
    while countdown:
        countdown -= 1
        sleep(.01)
        print "{}\r".format(list(KB.kbcheck())),

    print list(KB.kbcheck())

# class Keyme:

#     def __init__(self):
#         defined_keys = mykbcodes.KEYcode2description.keys()

#         #self.initial_values = GetKeyboardState()
#         pass



# TODO
# The keyboard checking func itself can be wrapped in a function so that the
# speed will benifit from a function closure


