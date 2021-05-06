from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from WeatherModule import *
from ClothesModule import *

# 타이틀
TITLE = "날씨 의상추천 프로그램"

# 윈도우 크기
WND_W = 800 
WND_H = 600

# Ui_Main 클래스 #####################################################################################
class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):        
        Main.setObjectName("Main")        

        # 각 UI 윈도우를 stack에 생성하여 self.QtStack.setCurrentIndex()을 이용하여 UI 윈도우를 이동할수있다.

        # QStackedLayout 생성
        self.QtStack = QtWidgets.QStackedLayout()

        # stack list 생성
        self.stack = []        
        
        # QWidget 생성하여 리스트에 추가
        for i in range(5):
            self.stack.append(QtWidgets.QWidget())            

        # UI 생성
        self.Window1UI()
        self.Window2UI()
        self.Window3UI()
        self.Window4UI()
        
        # QWidget을 QStackedLayout에 추가
        for st in self.stack:
            self.QtStack.addWidget(st)

    # 타이틀 UI
    def Window1UI(self):
        st = self.stack[0]
        st.resize(WND_W, WND_H)        
        st.setWindowTitle(TITLE) # 각 윈도우마다 다른 타이틀을 설정할수 있으나 본 코드는 모두 통일했다

        # 위젯을 위한 폰트
        font = QtGui.QFont()
        font.setFamily("돋움체")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)

        self.StartButton = QtWidgets.QPushButton(st)        
        self.StartButton.setGeometry(QtCore.QRect(100, 80, 597, 317))        
        self.StartButton.setStyleSheet("border-image:url(./이미지/중앙 사진.jpg);")
        #self.StartButton.setStyleSheet(
        #    "QPushButton{border-image:url(./이미지/중앙 사진.jpg);}"
        #    "QPushButton:pressed{ border-image:url(./이미지/남자.JPG);}")        
        self.MessageLabel(st, 250, 410, "오늘 뭐 입지?")

        # 종료 버튼
        self.QuitButton = QtWidgets.QPushButton(st)
        self.QuitButton.setText("종료")
        self.QuitButton.setGeometry(QtCore.QRect(270, 500, 250, 60))
        self.QuitButton.setFont(font)

    # 성별 선택 UI
    def Window2UI(self):
        st = self.stack[1]
        st.resize(WND_W, WND_H)
        st.setWindowTitle(TITLE)
        #st.setStyleSheet("background: green")

        st.FemaleButton = QtWidgets.QPushButton(st)
        #st.FemaleButton.setText("여자")
        st.FemaleButton.setGeometry(QtCore.QRect(130, 140, 250, 332))        
        st.FemaleButton.setStyleSheet("border-image:url(./이미지/여자.jpg);")        

        st.MaleButton = QtWidgets.QPushButton(st)
        #st.MaleButton.setText("남자")
        st.MaleButton.setGeometry(QtCore.QRect(430, 140, 250, 332))        
        st.MaleButton.setStyleSheet("border-image:url(./이미지/남자.jpg);")

        self.MessageLabel(st, 250, 30, "당신의 성별은?")

    # 지역 및 예보일 입력 UI
    def Window3UI(self):
        st = self.stack[2]
        st.resize(WND_W, WND_H)
        st.setWindowTitle(TITLE)

        # 위젯을 위한 폰트
        font = QtGui.QFont()
        font.setFamily("돋움체")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        
        # label
        self.NormalLabel(st, 180, 205, "도시이름")
        self.NormalLabel(st, 180, 305, " 며칠 후")

        # 도시이름 선택
        st.CityNameCbBox = QtWidgets.QComboBox(st)
        for c in self.city_list:
            st.CityNameCbBox.addItem(c)
        st.CityNameCbBox.move(320, 200)
        st.CityNameCbBox.resize(200, 40)
        st.CityNameCbBox.setFont(font)
        st.CityNameCbBox.activated.connect(self.CityNameCB_Event)                

        # 며칠후(예보일) 선택
        st.ForecastCbBox = QtWidgets.QComboBox(st)
        
        for i in range(8):
            day = "%d" % i
            st.ForecastCbBox.addItem(day)                

        st.ForecastCbBox.move(320, 300)                
        st.ForecastCbBox.resize(200, 40)
        st.ForecastCbBox.setFont(font)
        st.ForecastCbBox.activated.connect(self.ForecastCB_Event)
        self.forecastIndex = 0

        # 추천버튼
        st.RecommendButton = QtWidgets.QPushButton(st)
        st.RecommendButton.setText("의상 추천")
        st.RecommendButton.setGeometry(QtCore.QRect(275, 430, 250, 60))
        st.RecommendButton.setFont(font)

        self.MessageLabel(st, 250, 30, "오늘 뭐 입지?")

    # 날씨 및 추천 의상 보여주기 UI
    def Window4UI(self):
        st = self.stack[3]
        st.resize(WND_W, WND_H)        
        st.setWindowTitle(TITLE)
        #st.setStyleSheet("background: green")       
        
        st.ImageLabel = QtWidgets.QLabel(st)
        st.ImageLabel.setObjectName("image")        
        st.ImageLabel.move(100, 90)
        st.ImageLabel.resize(280, 470)

        # label
        st.DateLabel = QtWidgets.QLabel(st)
        st.WeatherLabel = QtWidgets.QLabel(st)        
        st.TempLabel = QtWidgets.QLabel(st)
        st.LikeCountLabel = QtWidgets.QLabel(st)
        st.WebLinkTextLabel = QtWidgets.QLabel(st)
        self.UpdateLabel(st.DateLabel, 420, 150, "데이트 당일 날짜 :", 12)
        self.UpdateLabel(st.WeatherLabel, 420, 175, "데이트 당일 날씨 :", 12)
        self.UpdateLabel(st.TempLabel, 420, 200, "데이트 당일 온도 :", 12)
        self.UpdateLabel(st.LikeCountLabel, 420, 225, "현재 추천하는 의상의 좋아요 수 : ", 12)
        self.UpdateLabel(st.WebLinkTextLabel, 420, 270, "의상 구매 링크 :", 10)

        # 웹 주소의 링크
        #weblink_url = '<a href="{0}">{1}'.format("https://www.google.co.kr/", "https://www.google.co.kr/")
        st.WebLinkLabel = QtWidgets.QLabel(st)        
        st.WebLinkLabel.linkActivated.connect(self.WebLink)
        #st.WebLinkLabel.setText('<a href="https://www.google.co.kr/">https://www.google.co.kr/</a>')        
        #st.WebLinkLabel.setText(weblink_url)
        st.WebLinkLabel.setOpenExternalLinks(True)
        st.WebLinkLabel.move(525, 270)

        self.MessageLabel(st, 250, 10, "오늘 이거 입지?!")

        # 좋아요 버튼
        st.LikeButton = QtWidgets.QPushButton(st)        
        st.LikeButton.setGeometry(QtCore.QRect(420, 340, 160, 160))        
        st.LikeButton.setStyleSheet("border-image:url(./이미지/좋아요.jpg);")        

        # 싫어요 버튼
        st.DislikeButton = QtWidgets.QPushButton(st)        
        st.DislikeButton.setGeometry(QtCore.QRect(600, 340, 160, 160))
        st.DislikeButton.setStyleSheet("border-image:url(./이미지/싫어요.png);")


    def MessageLabel(self, stack, x, y, msg):
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        stack.Label = QtWidgets.QLabel(stack)
        stack.Label.setFont(font)
        stack.Label.setObjectName("Label")
        stack.Label.setText(msg)
        stack.Label.move(x, y)

    def NormalLabel(self, stack, x, y, msg, font_size=24):
        font = QtGui.QFont()
        font.setFamily("돋움체")
        font.setPointSize(font_size)
        font.setBold(False)
        font.setWeight(50)
        stack.Label = QtWidgets.QLabel(stack)
        stack.Label.setFont(font)
        stack.Label.setObjectName("Label")
        stack.Label.setText(msg)
        stack.Label.move(x, y)

    def UpdateLabel(self, label, x, y, msg, font_size):
        font = QtGui.QFont()
        font.setFamily("돋움체")
        font.setPointSize(font_size)
        label.setFont(font)
        label.setObjectName("Label")
        label.setText(msg)
        label.move(x, y)

    def ForecastCB_Event(self, index):
        # 예보일을 저장         
        self.forecastDay = index        
        #print(self.stack3.ForecastCbBox.itemText(index))
        #print(self.stack3.ForecastCbBox.itemData(index))

    def CityNameCB_Event(self, index):
        # 도시이름 저장
        self.cityName = self.city_list[index]
        print(self.cityName)

    def WebLink(self, url):
        print(url)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

# Main 클래스 ########################################################################################
class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):        
        # 멤버 변수 초기화
        self.forecastDay  = 0
        self.cityName = "" 
        self.sex = ""     
        self.path = ""
        self.info_file = ""
        self.like_count = 0
        self.city_list = ["서울", "수원", "부산", "인천", "대전", "대구", "전주"]
        self.img_list = []
        
        super(Main, self).__init__(parent)        
        self.setupUi(self)        

        # 버튼의 함수 설정
        self.StartButton.clicked.connect(self.OpenWindow1)        
        self.QuitButton.clicked.connect(QtWidgets.qApp.quit) 
        self.stack[1].FemaleButton.clicked.connect(self.SelectFemale)
        self.stack[1].MaleButton.clicked.connect(self.SelectMale)
        self.stack[2].RecommendButton.clicked.connect(self.OpenWindow4)
        self.stack[3].LikeButton.clicked.connect(self.IncreaseLikeCount)
        self.stack[3].DislikeButton.clicked.connect(self.UpdateNextImage)        

    # 성별 선택
    def OpenWindow1(self):        
        self.QtStack.setCurrentIndex(1)    

    def SelectFemale(self):
        self.sex = "여자"
        self.OpenWindow3()

    def SelectMale(self):
        self.sex = "남자"
        self.OpenWindow3()

    # 도시, 예보일 선택
    def OpenWindow3(self):
        # 기본선택
        self.cityName = "서울" 
        self.forecastDay  = 0 
        self.stack[2].CityNameCbBox.setCurrentIndex(0)
        self.stack[2].ForecastCbBox.setCurrentIndex(0)

        self.QtStack.setCurrentIndex(2)
    
    # 추천 의상
    def OpenWindow4(self):
        date = datetime.today() + timedelta(days=self.forecastDay)
        date_str = date.strftime("%Y년 %m월 %d일".encode('unicode-escape').decode()).encode().decode('unicode-escape')        
        #print("도시 : %s , 예보일 : %d" % (self.cityName, self.forecastDay))

        # 날씨 API로 질의
        wa = WeatherApi(APIKEY)
        temp, desc = wa.QueryCityDay(self.cityName, self.forecastDay)
        temp = round(temp, 1) # 소수점 둘째자리 반올림, 첫째짜리만 표기 (소수점 둘째자리 이하가 존재할수있음)

        print("날씨 : %.1f %s" % (temp, desc))

        # 서식문자열로 만들고 Label 위젯 갱신 
        DateStr = "데이트 당일 날짜 : {0}".format(date_str)
        self.stack[3].DateLabel.setText(DateStr)
        print(DateStr)                

        WeatherStr = "데이트 당일 날씨 : {0}".format(desc)
        self.stack[3].WeatherLabel.setText(WeatherStr)
        print(WeatherStr)         
        
        TempStr = "데이트 당일 온도 : {:.1f}도".format(temp)
        self.stack[3].TempLabel.setText(TempStr)
        print(TempStr)         

        # 정보파일의 경로 만들기(0.txt)
        self.path = "./이미지/" + self.sex + "/"
        self.path += self.GetFolderName(temp) + "/"
        self.info_file = self.path + "0.txt"

        # 의상 객체 생성
        self.clothes = Clothes(self.info_file)
        best_list = self.clothes.GetBestList()        
        self.like_count = best_list[1]
        image_file = self.path + best_list[2]

        # 추천 의상 출력, 의상 구매 링크 생성, 좋아요 출력
        self.PutImageWebLink(best_list[0], image_file)
        self.UpdateLikeCount()

        self.QtStack.setCurrentIndex(3)

    # 추천 의상 출력, 의상 구매 링크 생성
    def PutImageWebLink(self, url, image_file):
        pixmap = QtGui.QPixmap(image_file)
        resize_pixmap = pixmap.scaled(280, 470) # 크기 조정
        self.stack[3].ImageLabel.setPixmap(QtGui.QPixmap(resize_pixmap))

        # 의상 구매 링크
        weblink_url = '<a href="{0}">{1}'.format(url, url[:40]) # 표기 url은 앞에서 40문자만 출력하도록 제한
        self.stack[3].WebLinkLabel.setText(weblink_url)

    # 좋아요 수 label 갱신
    def UpdateLikeCount(self):
        # 좋아요 수를 서식문자열로 만들기        
        LikeCountStr = "현재 추천하는 의상의 좋아요 수 : {0}".format(self.like_count)
        self.stack[3].LikeCountLabel.setText(LikeCountStr)
        print(LikeCountStr)        

    # 좋아요 수를 증가 시킴
    def IncreaseLikeCount(self):
        self.like_count += 1
        self.clothes.Like()
        self.clothes.Save(self.info_file)
        self.UpdateLikeCount()
        
        QMessageBox.information(self, "안내", "타이틀 화면으로 이동합니다.", QMessageBox.Yes)
        self.QtStack.setCurrentIndex(0) # 타이틀 화면으로 이동

    def UpdateNextImage(self):
        self.clothes.DisLike()

        best_list = self.clothes.GetBestList()
        self.like_count = best_list[1]       
        image_file = self.path + best_list[2]

        # 추천 의상 출력, 의상 구매 링크 생성, 좋아요 출력
        self.PutImageWebLink(best_list[0], image_file)
        self.UpdateLikeCount()

    def GetFolderName(self, temp):        
        if temp <= 10.0:
            return "10도이하"
        elif temp <= 17.0:
            return "10초과~17도이하"
        elif temp <= 25.0:
            return "17초과~25도이하"
        else:
            return "25도초과"

    def ReadText(self, file_name):
        file = open(file_name, mode='rt', encoding='utf-8')    
        url = file.readline()        
        file.close()
        return url


if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main()
    sys.exit(app.exec_())