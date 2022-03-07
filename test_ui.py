import sys
import time
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
import prj_function_directory as pfd
import handmouse
import cv2


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, Mainwindow, on_top=True):
        super(Ui_MainWindow, self).__init__()
        self.on_top = on_top
        self.MainWindow = MainWindow
        self.localPos = None
        self.setupUi(self.MainWindow)

    def setupUi(self, MainWindow):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1495, 782)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
                                      if self.on_top else QtCore.Qt.FramelessWindowHint)
        # FramelessWindowHint = 닫기 버튼 등 상단에 표시 되는 것들이 안 보이게 됨
        # WindowStaysOnTopHint = 윈도를 '항상 위에' 노출

        self.MainWindow.setWindowFlags(flags)

        # 투명 배경을 사용하게 위한 Attribute 설정
        self.MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1360, 380, 100, 100))
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"border-image: url(./img/2_painter_btn_img.png);\n"
"padding:7px;\n"
"}\n"
"QPushButton:disabled{\n"
"border-image: url(./img/2_painter_btn_img.png);\n"
"}\n"
"QPushButton:hover{\n"
"border-image: url(./img/2_painter_btn_img_2.png);\n"
"}\n"
"QPushButton:pressed{\n"
"border-image: url(./img/2_painter_btn_img_3.png);\n"
"}"
"")
        self.pushButton_2.setText("")
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1360, 640, 100, 100))
        self.pushButton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"border-image: url(./img/4_exit_btn_img.png);\n"
"padding:7px;\n"
"}\n"
"QPushButton:disabled{\n"
"border-image: url(./img/4_exit_btn_img.png);\n"
"}\n"
"QPushButton:hover{\n"
"border-image:url(./img/4_exit_btn_img_2.png);\n"
"}\n"
"QPushButton:pressed{\n"
"border-image:url(./img/4_exit_btn_img_3.png);\n"
"}"
"")
        self.pushButton_4.setText("")
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1360, 250, 100, 100))
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"border-image: url(./img/1_mouse_btn_img.png);\n"
"padding:7px;\n"
"}\n"
"QPushButton:disabled{\n"
"border-image: url(./img/1_mouse_btn_img.png);\n"
"}\n"
"QPushButton:hover{\n"
"border-image: url(./img/1_mouse_btn_img_2.png);\n"
"}\n"
"QPushButton:pressed{\n"
"border-image: url(./img/1_mouse_btn_img_3.png);\n"
"}"
"")
        self.pushButton.setText("")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1360, 510, 100, 100))
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"border-image: url(./img/3_keyboard_btn_img.png);\n"
"padding:7px;\n"
"}\n"
"QPushButton:disabled{\n"
"border-image: url(./img/3_keyboard_btn_img.png);\n"
"}\n"
"QPushButton:hover{\n"
"border-image:url(./img/3_keyboard_btn_img_2.png);\n"
"}\n"
"QPushButton:pressed{\n"
"border-image: url(./img/3_keyboard_btn_img_3.png);\n"
"}"
"")
        self.pushButton_3.setText("")
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 40, 1291, 721))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/grad_contour_for_control_region.png"))
        self.label.setObjectName("label")
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


def thread_cam():
    # 미디어파이프 라이브러리에서 제공하는 함수를 사용하기 위한 객체를 생성합니다.
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # 플래그 값을 초기화 합니다.
    flag = {'momentum': True}
    # 이벤트 값을 저장하는 변수를 초기화합니다.
    event_val = 'default'
    # 랜드마크의 무게 중심 좌표값을 저장하는 변수를 초기화합니다.
    momentum = (0, 0)
    # 외부입력 카메라의 해상도 값을 다음과 같은 크기로 설정합니다.
    cam_width, cam_height = 1440, 810 #FULL HD의 75% 사이즈
    # OpenCV 라이브러리를 이용하여 비디오 객체를 생성합니다.
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # 초당 프레임(FPS) 계산을 위해 현재 시간을 획득합니다.
        start_time = time.time()
        # 비디오 객체로부터 리턴 값(ret)과 영상(frame)을 가져옵니다.
        ret, frame = cap.read()
        # 영상을 좌우 반전하여 출력합니다.
        frame = cv2.flip(src=frame, flipCode=1)
        # 영상의 출력되는 사이즈를 조절합니다.
        frame = cv2.resize(src=frame, dsize=(cam_width, cam_height), interpolation=cv2.INTER_AREA)
        # 영상의 채널을 BGR 채널에서 RGB 채널로 변환합니다.
        frame = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)
        # 미디어파이프(mediapipe)의 함수에 현재 영상 정보를 입력으로 한 결과(return)를 받습니다.
        result = hands.process(frame)
        # 영상의 채널을 RGB 채널에서 BGR 채널로 변환합니다.
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # 미디어파이프 라이브러리로부터 획득한 결과 값(result.multi_hand_landmarks)을 mp_return_value 변수에 할당합니다.
        # 결과 값(result.multi_hand_landmarks)의 형태는 총 21개 랜드마크의 x, y, z 좌표를 가지고 있습니다.
        # visibility 데이터는 라이브러리 이슈가 있어서 제외하도록 합니다.
        mp_return_value = result.multi_hand_landmarks
        # mp_return_value 타입이 "None"이 아닌 경우에만 이하 스크립트를 실행합니다.
        if mp_return_value is not None:
            # 아래의 출력문(print)은 각 랜드마크의 x, y, z 좌표를 확인할 수 있습니다.
            """ print(result.multi_hand_landmarks) """
            # 1개 프레임(frame)에 대해서 각 랜드마크(최대 21개)에 대한 분석을 진행합니다.
            for landmark_index in mp_return_value:
                # 총 21개의 랜드마크가 갖고 있는 좌표(x, y) 데이터를 저장할 객체를 생성합니다.
                segment = np.zeros((21, 2))
                # 각 랜드마크(최대 21개)의 좌표 데이터 중 해상도를 벗어나는 값이 발생하는 경우, 이벤트 처리를 위한 플래그입니다.
                none_flag = False
                # 각 랜드마크의 좌표(x, y) 데이터를 행렬(segment)에 할당합니다.
                for idx, landmark in enumerate(landmark_index.landmark):
                    segment[idx] = landmark.x, landmark.y
                    # 랜드마크의 좌표가 해상도의 최대, 최소값을 벗어나는 경우, 플래그(none_flag)를 활성화 시켜서 이벤트 발생을 억제합니다.
                    if int(landmark.x * cam_width) < 0 or int(landmark.x * cam_width) > cam_width:
                        none_flag = True
                    if int(landmark.y * cam_height) < 0 or int(landmark.y * cam_height) > cam_height:
                        none_flag = True
                    # 비정상적인 랜드마크 좌표값이 확인되었을 경우에는 이후 프로세스를 진행하지 않고 다음 프레임(frame)을 분석합니다.
                    if none_flag:
                        event_val = 'default'
                        break
                if not none_flag:
                    """
                    momentum:       0번, 5번, 17번 랜드마크의 무게 중심 좌표값을 획득합니다.
                    event_val:      
                    """
                    momentum, event_val, switch = handmouse.calculate_loc_info(landmarks=segment)
                    print(f'event_val({switch}): {event_val}')

                    # x, y, sx, sy, h=int(512 * 0.15), w=int(512 * 0.15)

                    # tf_result = icon_in(momentum[0], momentum[1], 1630, 370)
                    # icon_control(tf_result, event_val)


        # 설정된 영상을 출력합니다. (Setup)
        if flag['momentum']:
            draw_point = tuple([int(momentum[0] * cam_width), int(momentum[1] * cam_height)])
            cv2.circle(img=frame, center=draw_point, radius=3, color=(255, 0, 0), thickness=3)

        cv2.imshow('frame', frame)
        cv2.moveWindow(winname='frame', x=int((screen_width / 2) - (cam_width / 2)), y=int((screen_height / 2) - (cam_height / 2)))

        # execute_event(event_val)

        # "Q"버튼을 누르면 프로세스를 종료합니다.
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()


#
# def execute_event(event):
#     if event == 'move':
#         pfd.move_event()
#     elif event == 'leftclick':
#         pfd.leftclick_event()
#     elif event == 'doubleclick':
#         pfd.doubleclick_event()
#     elif event == 'drag':
#         pfd.drag_event()
#     elif event == 'rightclick':
#         pfd.rightclick_event()
#     elif event == 'screenshow':
#         pfd.screenshot_event()
#     elif event == 'scroll':
#         pfd.scroll_event()
#     else:
#         pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()

    ####################################################################################################################
    # 백엔드 모듈을 가져옵니다.
    handmouse.initialize()

    import pyautogui
    global screen_width, screen_height
    screen_width, screen_height = pyautogui.size()

    # 외부입력 카메라를 사용하기 위한 멀티스레드를 실행합니다.
    from threading import Thread
    global switch

    thread_module_cam = Thread(target=thread_cam, name='thread_module_cam')
    thread_module_cam.daemon = True
    thread_module_cam.start()
    ####################################################################################################################


    sys.exit(app.exec_())

