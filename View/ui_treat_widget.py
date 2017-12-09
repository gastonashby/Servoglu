__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QColorDialog, QFrame
from PyQt5.QtGui import QColor
import types
import random

class Ui_TreatDockWidget(QtCore.QObject):

    def __init__(self):
        super(Ui_TreatDockWidget, self).__init__()
        self.slider = []
        self.label = []
        self.treat_vals = []
        self.tr_spins = []
        self.tr_names_value = {}

        self.r = lambda: random.randint(0,255)

    def get_new_color(self):
        return '#%02X%02X%02X' % (self.r(), self.r(), self.r())

    def setupUi(self, ControlsBox):
        self.parent = ControlsBox
        self.languageHash = self.parent.controller.languageSupport.languageHash
        ControlsBox.setObjectName('General Controls')
        self.ui_controls_box_widget = QtGui.QDockWidget(self.languageHash.__getitem__("lbl.Treatment"), ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)

        #
        self.house_layout = QtGui.QVBoxLayout()
        self.colors = []
        self.color_buttons = []
        self.tr_checks = []
        self.definite_treat()
        self.init_tr_sliders()
        self.init_tr_spins()
        self.house_layout.addSpacing(10)
        # self.init_time_label()

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)

        self.ui_controls_box_widget.setWidget(self.house_widget)
        self.house_layout.addSpacing(10)

        self.button_apply_tr = QtGui.QPushButton(self.languageHash.__getitem__("lbl.ApplyTreatment"))
        self.button_apply_tr.clicked.connect(self.apply_treat)
        self.house_layout.addWidget(self.button_apply_tr)
        self.button_apply_tr.setEnabled(False)

    def apply_treat(self):
        self.button_apply_tr.setEnabled(False)
        self.parent.controller.model.refresh_variables(self.tr_names_value)
        # Update treat values slider first
        for i in range(0, len(self.slider)):
            self.treat_vals[i] = self.slider[i].value()/100

        j = 0
        for i in range(len(self.slider), len(self.treat_vals)):
            self.treat_vals[i] = self.tr_spins[j].value()
            j += 1

        self.parent.controller.model.recalculate(self.parent.step)


    def init_tr_sliders(self):
        _i = 0
        sliderF = ""
        for userDef in self.parent.controller.model._u:
            if userDef.isSlider:
                if len(userDef.color) > 0:
                    self.colors.append(userDef.color)
                else:
                    self.colors.append(self.get_new_color())

                vbox = QtGui.QVBoxLayout()
                # vbox.addStretch(1)

                self.tr_names_value[userDef.name] = float(userDef.defaultValue)

                s_aux = QtGui.QSlider(QtCore.Qt.Horizontal)
                s_aux.setRange(float(userDef.minTreatment) * 100, float(userDef.maxTreatment) * 100)
                s_aux.setValue(float(userDef.defaultValue) * 100)
                s_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                s_aux.setToolTip(userDef.detailedDescription)

                l_aux = QtGui.QLabel()
                myFont = QtGui.QFont()
                myFont.setBold(True)
                l_aux.setFont(myFont)
                l_aux.setText(userDef.description + ' ' + str(float(s_aux.value() / 100)) + ' ' + userDef.unit)
                l_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                l_aux.setToolTip(userDef.detailedDescription)

                b_aux = QtGui.QPushButton("")
                b_aux.setMaximumWidth(15)
                b_aux.setMaximumHeight(15)
                b_aux.setStyleSheet('QPushButton {background-color:' + self.colors[_i] + ';}')
                b_aux.clicked.connect(eval("self.eqSliderChangeValue_" + str(_i)))
                self.color_buttons.append(b_aux)

                ch_aux = QtGui.QCheckBox("Visible")
                ch_aux.setChecked(1)
                ch_aux.stateChanged.connect(eval("self.eqSliderChangeVisibleValue_" + str(_i)))
                self.tr_checks.append(ch_aux)

                h_box_aux = QtGui.QHBoxLayout()
                h_box_aux.addWidget(ch_aux)
                h_box_aux.addWidget(b_aux)


                self.slider.append(s_aux)
                self.treat_vals.append(s_aux.value()/100)
                self.label.append(l_aux)
                vbox.addWidget(l_aux)
                vbox.addLayout(h_box_aux)
                vbox.addWidget(s_aux)

                self.house_layout.addLayout(vbox)
                vbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
                #self.house_layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
                self.house_layout.addSpacing(5)
                _i += 1

    def init_tr_spins(self):
        _i = 0
        _j = len(self.slider)
        for userDef in self.parent.controller.model._u:
            if userDef.graphAsTreatment and not userDef.isSlider:
                if len(userDef.color) > 0:
                    self.colors.append(userDef.color)
                else:
                    self.colors.append(self.get_new_color())

                myFont = QtGui.QFont()
                myFont.setBold(True)

                l_aux = QtGui.QLabel()
                lunit_aux = QtGui.QLabel()
                l_aux.setFont(myFont)
                spin = []

                if userDef.type == 'integer' or userDef.type == 'int':
                    spin = QtGui.QSpinBox()
                    spin.setFont(myFont)
                    spin.setRange(int(userDef.minTreatment), int(userDef.maxTreatment))
                    spin.setValue(int(userDef.defaultValue))
                    spin.setSingleStep(1)
                    self.treat_vals.append(int(userDef.defaultValue))
                    self.tr_names_value[userDef.name] = int(userDef.defaultValue)
                else:
                    spin = QtGui.QDoubleSpinBox()
                    spin.setRange(float(userDef.minTreatment), float(userDef.maxTreatment))
                    spin.setValue(float(userDef.defaultValue))
                    spin.setSingleStep((float(userDef.maxTreatment) - float(userDef.minTreatment)) / 100)
                    self.treat_vals.append(float(userDef.defaultValue))
                    self.tr_names_value[userDef.name] = float(userDef.defaultValue)

                spin.valueChanged.connect(eval("self.trSpinChangeValue_" + str(_i)))
                self.tr_spins.append(spin)
                l_aux.setText(userDef.description)
                l_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                l_aux.setToolTip(userDef.detailedDescription)

                lunit_aux.setText(userDef.unit)
                lunit_aux.setFont(myFont)

                vbox = QtGui.QHBoxLayout()
                vbox.addWidget(l_aux)
                vbox.addWidget(spin)
                vbox.addWidget(lunit_aux)
                self.house_layout.addLayout(vbox)

                b_aux = QtGui.QPushButton("")
                b_aux.setMaximumWidth(15)
                b_aux.setMaximumHeight(15)
                b_aux.setStyleSheet('QPushButton {background-color:' + self.colors[_j] + ';}')
                b_aux.clicked.connect(eval("self.eqSliderChangeValue_" + str(_j)))
                self.color_buttons.append(b_aux)

                ch_aux = QtGui.QCheckBox("Visible")
                ch_aux.setChecked(1)
                ch_aux.stateChanged.connect(eval("self.eqSliderChangeVisibleValue_" + str(_j)))
                self.tr_checks.append(ch_aux)

                h_box_aux = QtGui.QHBoxLayout()
                h_box_aux.addWidget(ch_aux)
                h_box_aux.addWidget(b_aux)

                vbox.addLayout(h_box_aux)

                _i += 1
                _j += 1


    def get_sliders_vals(self):
        return self.treat_vals


    def definite_treat(self):
        _i = 0
        _j = 0
        for eq in self.parent.controller.model._u:
            if eq.graphAsTreatment:

                controlFunc, _c_f_aux = self.parent.controller.model.code.definite_slider_change_color(_i)
                exec(controlFunc)
                exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")

                controlFunc, _c_f_aux = self.parent.controller.model.code.definite_slider_change_visible(_i)
                exec(controlFunc)
                exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")

                if not eq.isSlider:
                    controlFunc, _c_f_aux = self.parent.controller.model.code.definite_spin_change_value(eq, _j, eq.defaultValue)
                    exec(controlFunc)
                    exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")
                    _j += 1
                _i += 1

    def show_slider_att_changing(self, slider_id, type):

        if type == 'COLOR':
            color = QColorDialog.getColor()

            if color.isValid():
                self.colors[slider_id] = color.name()
                self.parent.controller.handler_change_graph_color(slider_id, "TREAT", self.colors[slider_id])
                self.color_buttons[slider_id].setStyleSheet('QPushButton {background-color:' + self.colors[slider_id] + ';}')
        elif type == 'VISIBLE':
            print(self.tr_checks[slider_id].isChecked(), slider_id)

            self.parent.simulated_tr[slider_id] = self.tr_checks[slider_id].isChecked()

            if self.tr_checks[slider_id].isChecked():
                self.parent.all_treat_curves[slider_id] = self.parent.create_treat_curve(slider_id, self.parent.controller.model._u[slider_id].name)
                self.parent.all_treat_curves[slider_id].setData(self.parent.xDataGraf[:self.parent.indexGr + 1],
                                                   self.parent.treatment[slider_id])
            else:
                self.parent.all_treat_curves[slider_id].clear()