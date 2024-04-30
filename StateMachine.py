import time
from typing import Callable

import pyautogui

import service
from config import *


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
            self.__check_state()
            # delay
            time.sleep(self.__time_out_s)
            self.__do_action()
            time.sleep(self.__time_out_s)
        pass

    # 检查、设置当前状态
    def __check_state(self):
        # 检查是否在课程列表页面
        pos = pyautogui.locateOnScreen(class_page_tag_img_path, confidence=0.8)
        if pos is not None:
            # pyautogui.moveTo(pos.left, pos.top)
            print("pos : ", pos.top, pos.left, pos.width, pos.height)  # 968 * 69
            self.__time_out_s = 0.1
            self.__state = State.ClassListPage
            print("state is class list page")
            return

        # 检查是否在课程页面
        pos = pyautogui.locateOnScreen(class_tag_img_path, confidence=0.8)
        if pos is not None:
            # pyautogui.moveTo(pos.left, pos.top)
            print("课程页面 pos : ", pos.top, pos.left, pos.width, pos.height)

            # 检查是否在播放
            ppos = pyautogui.locateOnScreen(class_processing_btn_img_path, confidence=0.8)
            if ppos is not None:
                # pyautogui.moveTo(ppos.left, ppos.top)
                print("pos : ", ppos.top, ppos.left, ppos.width, ppos.height)
                self.__time_out_s = 0.1
                self.__state = State.ClassPage_Playing
                print("state is class page playing")
                return
            # 检查是否有未播放视频
            ppos = pyautogui.locateOnScreen(class_start_btn_img_path, confidence=0.8)
            if ppos is not None:
                pyautogui.click(ppos.left + 60, ppos.top)
                print("点击下一课 pos : ", ppos.left, ppos.top, ppos.width, ppos.height)
                self.__time_out_s = 0.1
                self.__state = State.ClassPage_Playing
                print("next, state is class page playing")
                return

            self.__state = State.ClassPage_Over
            self.__time_out_s = 0.2
            print("current class is over, state is class page over")
            return

        print("state is unknown")
        self.__state = State.UnKnown
        self.__time_out_s *= 2
        if self.__time_out_s > 1.6:
            self.__time_out_s = 1.6
        pass

    def __do_action(self):
        if self.__state == State.UnKnown:
            return

        if self.__state == State.ClassListPage:
            pos = pyautogui.locateOnScreen(enter_tag_img_path, confidence=0.8)
            if pos is None:
                self.__state = State.UnKnown
                return
            # pyautogui.moveTo(pos.left + 32, pos.top + 32)
            # time.sleep(30)
            pyautogui.click(pos.left + 32, pos.top + 30)
            print("点击进入课堂页面 click enter")
            self.__state = State.UnKnown
            self.__time_out_s = 5

        if self.__state == State.ClassPage_Playing:
            pos = pyautogui.locateOnScreen(pause_img_path, confidence=0.8)
            if pos is not None:
                print("is playing")
                pyautogui.moveTo(pos.left + 70, pos.top + 25)
                self.__time_out_s = 5
                return
            pos = pyautogui.locateOnScreen(play_img_path, confidence=0.9)
            if pos is None:
                pos = pyautogui.locateOnScreen(class_tag_img_path, confidence=0.8)
                if pos is None:
                    self.__state = State.UnKnown
                    print("in class page but not fond tag need image debug")
                    return
                pyautogui.moveTo(pos.left + 150, pos.top + 500)
                print("wait for next time")
                self.__time_out_s = 0.7
                return
            pyautogui.click(pos.left + 28, pos.top + 25)
            print("点击播放按钮, pos : ", pos.left, pos.top)
            self.__time_out_s = 145
            return

        if self.__state == State.ClassPage_Over:
            pos = pyautogui.locateOnScreen(close_img_path, confidence=0.8)
            if pos is None:
                print("in class page over but not fond close button need image debug")
                return
            pyautogui.click(pos.left + 10, pos.top + 10)
            print("点击关闭窗口按钮 click close")
            pyautogui.sleep(1)
            pyautogui.press("F5")
            self.__state = State.UnKnown
            self.__time_out_s = 5

        pass


type Handler = Callable[[], tuple[State, float]]


class ScriptStateMachine:
    def __init__(self):
        self.__active = True
        self.__state_handlers = {}

    def register(self, state: State, handler: Handler):
        self.__state_handlers[state] = handler
        pass

    def run(self, state: State):
        while self.__active:
            next_state, time_out = self.__state_handlers[state]()
            pyautogui.sleep(time_out)
            state = next_state

    def close(self):
        self.__active = False


class Service:
    def __init__(self):
        self.__state_machine = ScriptStateMachine()
        self.__state_machine.register(State.UnKnown, service.service_unknown)
        self.__state_machine.register(State.ClassListPage, service.service_class_list)
        self.__state_machine.register(State.ClassPage_Playing, service.service_class_playing)
        self.__state_machine.register(State.ClassPage_Over, service.service_class_over)

    def run(self):
        self.__state_machine.run(State.UnKnown)

    def close(self):
        self.__state_machine.close()
