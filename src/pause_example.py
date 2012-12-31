#!/usr/bin/env python

import sys, os
from os.path import join, getsize

from PyQt4 import QtCore, QtGui

#-------------------------------------------------------------------------------
# class
#-------------------------------------------------------------------------------
class Runner(QtCore.QThread):

	def __init__(self, lock, parent=None):
		QtCore.QThread.__init__(self)

		self.lock               = lock
		self.stopped            = False
		self.mutex              = QtCore.QMutex()
		self.completed          = False
		self.paused             = False
		self.rootDir            = ""



	def initialize(self):
		self.stopped            = False
		self.completed          = False
		self.paused             = False



	def run(self):
		print "Runner.run() ..."
		self.runTask()
		self.stop()
		self.emit(QtCore.SIGNAL("finished(bool)"), self.completed)



	def stop(self):
		print "Runner.NEW_stop() ..."
		with QtCore.QMutexLocker(self.mutex):
			self.stopped    = True



	def pause(self, theBool=True):
		print "Runner.pause() ..."

		if theBool == False:  # pause task
			try:
				self.mutex.lock()
				self.paused     = True
			finally:
				self.mutex.unlock()

		else: # resume processing
			try:
				self.mutex.lock()
				self.paused     = False
			finally:
				self.mutex.unlock()
			
			

	def isStopped(self):
		try:
			self.mutex.lock()
			return self.stopped
		finally:
			self.mutex.unlock()



	def runTask(self):
		progressStr        = ""

		if self.isStopped():
			return
		
		# set walk dir
		for root, dirs, files in os.walk(self.rootDir):

			if self.isStopped():
				return

			while(self.paused):
				QtCore.QThread.msleep(100)
			
			try:
				theSum             = sum(getsize(join(root, name)) for name in files),
				lenFiles           = len(files)
				progressStr        = "%s consumes: %d bytes in %d non-directory files" % (root, theSum[0], lenFiles)
			except OSError:
				pass

#			self.emit(QtCore.SIGNAL("setProgress(string)"), progressStr)
			self.emit(QtCore.SIGNAL("setProgress(PyQt_PyObject)"), progressStr)

		# completed
		self.completed     = True

		return 0



	def setRootDir(self, theDir):
		self.rootDir       = theDir



#-------------------------------------------------------------------------------
# class
#-------------------------------------------------------------------------------
class ConfirmDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self)
		

		# kill widgets
		self.restartButton      = QtGui.QRadioButton(self.tr("Restart task"))
		self.killButton         = QtGui.QRadioButton(self.tr("Kill task"))
		self.killButton.setChecked(True)
		self.killLayout         = QtGui.QVBoxLayout()
		self.killLayout.addWidget(self.restartButton)
		self.killLayout.addWidget(self.killButton)
		
		# confirm widgets
		self.okButton           = QtGui.QPushButton(self.tr("OK"))
		self.cancelButton       = QtGui.QPushButton(self.tr("Cancel"))
		self.confirmLayout      = QtGui.QHBoxLayout()
		self.confirmLayout.addWidget(self.okButton)
		self.confirmLayout.addWidget(self.cancelButton)

		# dialog layout
		self.formLayout         = QtGui.QVBoxLayout()
		self.formLayout.addLayout(self.killLayout)
		self.formLayout.addLayout(self.confirmLayout)
		self.setLayout(self.formLayout)



		# signals/slots
		# ------------------------------------------------
		self.connect(self.cancelButton,     QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))
		self.connect(self.okButton,		    QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()"))
		
		
		


#-------------------------------------------------------------------------------
# class
#-------------------------------------------------------------------------------
class ThreadTest(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self)
		

		self.rootLabel  	    = QtGui.QLabel(self.tr("Root Dir"))
		self.rootEdit           = QtGui.QLineEdit()
		self.rootLayout         = QtGui.QHBoxLayout()
		self.rootLayout.addWidget(self.rootLabel)
		self.rootLayout.addWidget(self.rootEdit)

		self.startButton        = QtGui.QPushButton(self.tr("Start"))
		self.pauseButton        = QtGui.QPushButton(self.tr("Pause"))
		self.pauseButton.setCheckable(True)
		self.stopButton         = QtGui.QPushButton(self.tr("Stop"))
		self.buttonLayout       = QtGui.QHBoxLayout()
		self.buttonLayout.addWidget(self.startButton)
		self.buttonLayout.addWidget(self.pauseButton)
		self.buttonLayout.addWidget(self.stopButton)

		self.formLayout         = QtGui.QHBoxLayout()
		self.formLayout.addLayout(self.rootLayout)
		self.formLayout.addLayout(self.buttonLayout)
		self.setLayout(self.formLayout)


		# signals/slots
		# ------------------------------------------------
		self.startButton.clicked.connect(self.startTask)
		self.connect(self.pauseButton, QtCore.SIGNAL("toggled(bool)"), self.pauseTask)
		self.stopButton.clicked.connect(self.stopTask)
		

		# init runner object
		# ------------------------------------------------
		self.lock        = QtCore.QReadWriteLock()
		self.runner      = Runner(self.lock, self)

#		self.connect(self.runner, QtCore.SIGNAL("setProgress(string)"), self.setProgress)
		self.connect(self.runner, QtCore.SIGNAL("setProgress(PyQt_PyObject)"), self.setProgress)
		self.connect(self.runner, QtCore.SIGNAL("finished(bool)"), self.finished)



	def setProgress(self, theString):
		print "setProgress: ", theString



	def finished(self, theBool):
		print "finished: ", theBool



	def startTask(self):
		self.runner.setRootDir(str(self.rootEdit.text()))
		self.runner.start()



	def pauseTask(self, isPaused):
		if isPaused:
			self.pauseButton.setText("Resume")
			self.runner.pause(False)  # reverse polarity of theBool
		else:
			self.pauseButton.setText("Pause")
			self.runner.pause(True)




	def stopTask(self):

		# stop task
		if self.runner.isRunning():
			self.runner.stop()

		# reset button text
		self.stopButton.setText("Restart/Kill...")
		if not self.runner.isRunning():

			# allow restart or kill
			form = ConfirmDialog()
			form.setWindowTitle(self.tr("Confirm"))

			if form.exec_():
				if form.restartButton.isChecked():
					self.runner.initialize()
					self.startTask()
					
				elif form.killButton.isChecked():
					self.stopButton.setText("Stop")
					if self.runner.isRunning():
						self.runner.stop()

				else:
					pass

			

		
		
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	form = ThreadTest()
	form.setWindowTitle("Thread Test")
	form.show()
	sys.exit(app.exec_())
	
