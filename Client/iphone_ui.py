import os, sys
import json
import socket
import requests
​
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime
​
​
class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
​
    def initUI(self):
​
        self.setObjectName("Iphone_Instagram")
        self.resize(448, 875)
        self.setFixedSize(448, 875)
        self.setStyleSheet("background-color: rgb(225, 225, 225);")
​
        # ********** ********** label_2 ********** **********
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(-10, 0, 461, 881))
        self.label_2.setStyleSheet("image: url(iphone_instagram2.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
​
        # ********** ********** label ********** **********
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(40, 230, 361, 361))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
​
        # ********** ********** pushButton ********** **********
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(420, 860, 21, 20))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "image: url(Button.JPG);")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.NextImage)
​
        # ********** ********** pushButton2 ********** **********
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(42, 606, 41, 31))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "image: url(heart.png);")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.PushHeart)
​
        # ********** ********** Execute ********** **********
        self.center()  # ** 창을 화면의 정 가운데에 위치 **
        self.show()
​
​
​
        # 해당 이미지 파일 json 읽기
        with open('data.json', 'r') as f:
            self.image_info = json.load(f)
        # image_info = json.dump(json_data)
        # image_info : data.json파일 내용
​
        self.number = 0
        self.filename = str(self.number) + ".jpg"
        image = QtGui.QImage(self.filename)
        if image.width() > 361:
            image = image.scaledToWidth(361)
        if image.height() > 361:
            image = image.scaledToHeight(361)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
​
        self.time = QTime.currentTime()
        self.start = self.time.toString('hh.mm.ss.zzz')
​
​
​
    def NextImage(self):
        self.time = QTime.currentTime()
        self.end = self.time.toString('hh.mm.ss.zzz')
​
        start_hour = int(self.start[:2])
        end_hour = int(self.end[:2])
        start_min = int(self.start[3:5])
        end_min = int(self.end[3:5])
        start_sec = int(self.start[6:8])
        end_sec = int(self.end[6:8])
        start_zz = int(self.start[9:11])
        end_zz = int(self.end[9:11])
​
        total_sec = 0
        total_zz = 0
​
        if start_zz > end_zz:
            end_sec -= 1
            end_zz += 100
        total_zz += (end_zz - start_zz)
​
        if (end_sec == -1):
            end_sec += 1
        if start_sec > end_sec:
            end_min -= 1
            end_sec += 60
        total_sec += (end_sec - start_sec)
​
        if (end_min == -1):
            end_min += 1
        if start_min > end_min:
            end_hour -= 1
            end_min += 60
        total_sec += (end_min - start_min) * 60
        total_sec += (end_hour - start_hour) * 3600
​
        total = str(total_sec) + "." + str(total_zz)
        print(self.filename, "/", total)
​
        # 시간과 데이터 data.json에서 수정
        self.image_info[self.filename]["consumed_time"] = int(total)
​
        # 다음 사진 시간 측정 시작
        self.time = QTime.currentTime()
        self.start = self.time.toString('hh.mm.ss.zzz')
​
        if self.number < 40:
            self.number = self.number + 10
        else:
            self.number = self.number - 39
​
        self.filename = str(self.number) + ".jpg"
        image = QtGui.QImage(self.filename)
        if image.width() > 361:
            image = image.scaledToWidth(361)
        if image.height() > 361:
            image = image.scaledToHeight(361)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
​
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "image: url(heart.png);")
​
​
    def PushHeart(self):
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "image: url(heart2.png);")
​
        if (self.image_info[self.filename]["like_flag"] == 1):
            # 이미 한번 누른경우, 초기화 (0)
            self.image_info[self.filename]["like_flag"] = 0
        else:  # 좋아요가 처음인 경우
            self.image_info[self.filename]["like_flag"] = 1
            print(self.filename, "Like it!")
​
​
    def web_request(self, method_name, url, dict_data, is_urlencoded=True):
        # Web GET or POST request를 호출 후 그 결과를 dict형으로 반환
​
        method_name = method_name.upper()  # 메소드이름을 대문자로 바꾼다
        if method_name not in ('GET', 'POST'):
            raise Exception('method_name is GET or POST plz...')
        if method_name == 'GET':  # GET방식인 경우
            response = requests.get(url=url, params=dict_data)
        elif method_name == 'POST':  # POST방식인 경우
            if is_urlencoded is True:
                response = requests.post(url=url, data=dict_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            else:
                response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})
        dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                     'Content-Type': response.headers['Content-Type']}
        if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
            return {**dict_meta, **response.json()}
        else:  # 문자열 형태인 경우
            return {**dict_meta, **{'text': response.text}}
​
​
    def sendData(self):
        url = 'http://127.0.0.1:5000/userAction'  # 접속할 사이트주소 또는 IP주소를 입력한다
        data = {'data': data.json}  # 요청할 데이터
        response = web_request(method_name='POST', url=url, dict_data=data)
​
​
    def center(self):
        ct = self.frameGeometry()
        ct2 = QtWidgets.QDesktopWidget().availableGeometry().center()
        ct.moveCenter(ct2)
        self.move(ct.topLeft())
​
​
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())