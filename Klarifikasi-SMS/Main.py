from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication
from PyQt5.QtCore import QBasicTimer


class BacaData(QWidget):
	def __init__(self):
		super().__init__()


		self.progressBar = QProgressBar(self)
		self.progressBar.setGeometry(30, 40, 200, 25)
        # self.startProgress()
		self.btnStart = QPushButton('Start', self)
		self.btnStart.move(30, 80)
		self.btnStart.clicked.connect(self.startProgress) 
		self.timer = QBasicTimer()
		self.step = 0

	def startProgress(self):
		if self.timer.isActive():
			self.timer.stop()
			self.btnStart.setText('Start')
		else:
			self.timer.start(100, self)
			self.btnStart.setText('Stop')

	def timerEvent(self, event):
		if self.step >= 100:
			self.timer.stop()
			self.btnStart.setText('Lanjut')
			return

		self.step +=1
		self.progressBar.setValue(self.step)

    

if __name__=='__main__':
	app = QApplication(sys.argv)
	demo = BacaData()
	demo.show()

	sys.exit(app.exec_())



# def inputSMS():
#     v  = call.lineEdit.toPlainText() 
#     v2 = call.lineEdit_2.text()
#     arr = [v]
#     print("sms anda:"+str(arr))


# app=QtWidgets.QApplication([])
# call=uic.loadUi("klarifikasi_sms.ui")
# call.submit.clicked.connect(inputSMS)

# call.show()
# app.exec()