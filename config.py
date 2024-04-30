import enum
import os

class_page_tag_img_path = os.getcwd() + "\\resource\\class_page_tag.png"
enter_img_path = os.getcwd() + "\\resource\\enter.png"
enter_tag_img_path = os.getcwd() + "\\resource\\enter_tag.png"

class_tag_img_path = os.getcwd() + "\\resource\\class_tag.png"
class_start_btn_img_path = os.getcwd() + "\\resource\\class_start_btn.png"
class_complete_btn_img_path = os.getcwd() + "\\resource\\complete.png"
class_processing_btn_img_path = os.getcwd() + "\\resource\\processing.png"

play_img_path = os.getcwd() + "\\resource\\play.png"
pause_img_path = os.getcwd() + "\\resource\\pause.png"
close_img_path = os.getcwd() + "\\resource\\close.png"


class State(enum.Enum):
    UnKnown = 0
    ClassListPage = 1
    ClassPage_Playing = 2
    ClassPage_Over = 3
