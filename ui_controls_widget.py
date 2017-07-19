__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules

# import 3rd party libraries
from PyQt5 import QtCore, QtGui


class Ui_GeneralControlsWidget(QtCore.QObject):

    def __init__(self):
        super(Ui_GeneralControlsWidget, self).__init__()


    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('General Controls')
        self.ui_controls_box_widget = QtGui.QDockWidget(ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.ui_controls_box_widget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

        #
        self.house_layout = QtGui.QVBoxLayout()

        self.timeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.timeSlider.setMinimum(1)
        self.timeSlider.setMaximum(1000)
        self.timeSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.timeSlider.setValue(500)
        self.timeSlider.setTickInterval(100)

        self.timeSliderLbl = QtGui.QLabel()
        self.timeSliderLbl.setText('1 simulated minute every 500 ms')


        self.btnPlayStop = QtGui.QPushButton('Play')
        self.btnNext = QtGui.QPushButton('Next')
        self.btnReset = QtGui.QPushButton('Reset')
        #
        self.house_layout.addWidget(self.timeSliderLbl)
        self.house_layout.addWidget(self.timeSlider)

        self.house_layout.addWidget(self.btnPlayStop)
        self.house_layout.addWidget(self.btnNext)
        self.house_layout.addWidget(self.btnReset)
        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)
        #
        self.ui_controls_box_widget.setWidget(self.house_widget)
