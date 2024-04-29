import os

import cv2

import State


def debug_info():
    print("running dir : ", os.getcwd())
    print("opencv version : ", cv2.__version__)


# main
if __name__ == "__main__":
    debug_info()
    loop = State.StateMachine()
    loop.run()
