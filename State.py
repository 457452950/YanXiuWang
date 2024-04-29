import enum
import os
import time
import cv2
import numpy as np
import pyautogui

class_page_tag_img_path = os.getcwd() + "\\resource\\class_page_tag.png"
class_start_btn_img_path = os.getcwd() + "\\resource\\class_start_btn.png"
class_tag_img_path = os.getcwd() + "\\resource\\class_tag.png"
play_img_path = os.getcwd() + "\\resource\\play.png"
pause_img_path = os.getcwd() + "\\resource\\pause.png"
enter_img_path = os.getcwd() + "\\resource\\enter.png"


class State(enum.Enum):
    UnKnown = 0
    ClassListPage = 1
    ClassPage_Playing = 2
    ClassPage_Pause = 2
    ClassPage_Over = 2


# 状态机
class StateMachine:
    def __init__(self):
        self.__state = State.UnKnown
        self.__time_out_s = 0.1
        self.__active = True

    def run(self):
        self.__loop()
        pass

    def __loop(self):
        while self.__active:
            self.check_state()
            # delay
            time.sleep(self.__time_out_s)
        pass

    # 检查、设置当前状态
    def check_state(self):
        pos = pyautogui.locateOnScreen(class_page_tag_img_path, confidence=0.8)
        if pos is not None:
            pyautogui.moveTo(pos.left, pos.top)
            print("pos : ", pos.top, pos.left, pos.width, pos.height)  # 968 * 69
            self.__time_out_s = 0.1
            self.__state = State.ClassListPage
            print("state is class list page")
            return

        pos = pyautogui.locateOnScreen(class_tag_img_path, confidence=0.8)
        if pos is not None:
            pyautogui.moveTo(pos.left, pos.top)
            print("pos : ", pos.top, pos.left, pos.width, pos.height)

            ppos = pyautogui.locateOnScreen(pause_img_path)
            if ppos is not None:
                pyautogui.moveTo(ppos.left, ppos.top)
                print("pos : ", ppos.top, ppos.left, ppos.width, ppos.height)
                self.__time_out_s = 0.1
                self.__state = State.ClassPage_Playing
                print("state is class page playing")
                return

            ppos = pyautogui.locateOnScreen(play_img_path)
            if ppos is not None:
                pyautogui.moveTo(ppos.left, ppos.top)
                print("pos : ", ppos.top, ppos.left, ppos.width, ppos.height)
                self.__time_out_s = 0.1
                self.__state = State.ClassPage_Pause
                print("state is class page pause")
                return

            pyautogui.moveTo(pos.left + 100, pos.top + 600)
            self.__state = State.UnKnown
            self.__time_out_s = 0.4
            return

        print("state is unknown")
        self.__state = State.UnKnown
        self.__time_out_s *= 2
        if self.__time_out_s > 2:
            self.__time_out_s = 2
        pass
