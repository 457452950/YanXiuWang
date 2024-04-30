from StateMachine import *
from config import *

service_unknown_time_out: float = 0.1


def service_unknown() -> tuple[State, float]:
    global service_unknown_time_out

    # 检查是否在课程列表页面
    pos = pyautogui.locateOnScreen(class_page_tag_img_path, confidence=0.8)
    if pos is not None:
        # pyautogui.moveTo(pos.left, pos.top)
        print("pos : ", pos.top, pos.left, pos.width, pos.height)  # 968 * 69
        return State.ClassListPage, 0.1

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
            print("state is class page playing")
            return State.ClassPage_Playing, 0.1
        # 检查是否有未播放视频
        ppos = pyautogui.locateOnScreen(class_start_btn_img_path, confidence=0.8)
        if ppos is not None:
            pyautogui.click(ppos.left + 60, ppos.top)
            print("点击下一课 pos : ", ppos.left, ppos.top, ppos.width, ppos.height)
            print("next, state is class page playing")
            return State.ClassPage_Playing, 0.1

        print("current class is over, state is class page over")
        return State.ClassPage_Over, 0.2

    print("state is unknown")
    service_unknown_time_out *= 2
    if service_unknown_time_out > 1.6:
        service_unknown_time_out = 1.6
    return State.UnKnown, service_unknown_time_out


def service_class_list() -> tuple[State, float]:
    pos = pyautogui.locateOnScreen(enter_tag_img_path, confidence=0.8)
    if pos is None:
        return State.UnKnown, 0.1
    # pyautogui.moveTo(pos.left + 32, pos.top + 32)
    # time.sleep(30)
    pyautogui.click(pos.left + 32, pos.top + 30)
    print("点击进入课堂页面 click enter")
    return State.UnKnown, 5


def service_class_playing() -> tuple[State, float]:
    pos = pyautogui.locateOnScreen(pause_img_path, confidence=0.8)
    if pos is not None:
        print("is playing")
        pyautogui.moveTo(pos.left + 70, pos.top + 25)
        return State.ClassPage_Playing, 5
    pos = pyautogui.locateOnScreen(play_img_path, confidence=0.9)
    if pos is None:
        pos = pyautogui.locateOnScreen(class_tag_img_path, confidence=0.8)
        if pos is None:
            print("in class page but not fond tag need image debug")
            return State.UnKnown, 0.1
        pyautogui.moveTo(pos.left + 150, pos.top + 500)
        print("wait for next time")
        return State.ClassPage_Playing, 0.7
    pyautogui.click(pos.left + 28, pos.top + 25)
    print("点击播放按钮, pos : ", pos.left, pos.top)
    return State.ClassPage_Playing, 145


def service_class_over() -> tuple[State, float]:
    pos = pyautogui.locateOnScreen(close_img_path, confidence=0.8)
    if pos is None:
        print("in class page over but not fond close button need image debug")
        return State.UnKnown, 0.1
    pyautogui.click(pos.left + 10, pos.top + 10)
    print("点击关闭窗口按钮 click close")
    pyautogui.sleep(1)
    pyautogui.press("F5")
    return State.UnKnown, 5
