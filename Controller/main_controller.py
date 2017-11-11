import os.path
import sys

#from Model import Plot2 as self.model
from Model.LanguageParser import LanguageParser
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from Model.Model import Model

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


class Controller():
    def __init__(self, window):
        self.model = Model()
        self.window = window
        self.dataFormat = self.model.code
        # Initialize language hash with English as default language
        if len(sys.argv) > 1:
            self.languageSupport = LanguageParser("SystemLanguageSupport.csv", sys.argv[1])
        else:
            self.languageSupport = LanguageParser("SystemLanguageSupport.csv", "Español")

        self.version = self.languageSupport.languageHash.__getitem__("lbl.Version")
        self.eq_convert_factors = []
        self.tr_convert_factors = []
        self.np = self.model.np

    def convertMs(self, mili):
        # ms = mili % 1000
        s = (mili / 1000) % 60
        m = (mili / (1000 * 60)) % 60
        h = (mili / (1000 * 60 * 60)) % 24
        d = str(int((mili / (1000 * 60 * 60 * 24))))
        if h < 10:
            h = "0" + str(int(h))
        else:
            h = str(int(h))

        if m < 10:
            m = "0" + str(int(m))
        else:
            m = str(int(m))

        if s < 10:
            s = "0" + str(int(s))
        else:
            s = str(int(s))

        # if ms < 10:
        #     ms = "00" + str(int(ms))
        # elif ms < 100:
        #     ms = "0" + str(int(ms))
        # else:
        #     ms = str(int(ms))

        return d + ":" + h + ":" + m + ":" + s #+ ":" + ms

    def change_treatment(self, case,treatment, t):
        const = 100
        if case == 99:
            if treatment == "a":
                if t < 60:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0) #Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(260 * const) #Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0) #Enteral tube feeding
                elif t >= 60 and t < 120:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0.02 * const) #Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(110 * const) #Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0) #Enteral tube feeding
                else:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0.012 * const) #Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(25 * const) #Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0) #Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.5*const)  # Insulin sensitivity
                    #0.5 anduvo bien
            if treatment == "b":
                if t < 60:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0) #Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(260 * const) #Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0.051*const) #Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.5 * const)
                elif t >= 60 and t < 120:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0 * const) #Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(0 * const) #Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0.051*const) #Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.8     * const)
                else:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0.012 * const) #Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(60 * const) #Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0) #Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.7*const)  # Insulin sensitivity
                    #0.5 anduvo bien
            if treatment == "c":
                if t < 60:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(25 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0 * const)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.6 * const)
                elif t >= 60 and t < 120:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(0 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0 * const)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.5 * const)
                else:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(0 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.5 * const)  # Insulin sensitivity
        elif case == 93:
            if treatment == "a":
                if t < 60:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(30 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.65 * const)  # Insulin sensitivity
                elif t >= 60 and t < 120:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(55 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.45 * const)  # Insulin sensitivity
                else:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(30 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.45 * const)  # Insulin sensitivity

            if treatment == "b":
                if t < 60:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(65 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0.051 * const)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.5 * const)
                elif t >= 60 and t < 120:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(80 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0.0 * const)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.5 * const)
                else:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0.0 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(50 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.5 * const)  # Insulin sensitivity
                    # 0.5 anduvo bien
            if treatment == "c":
                if t < 60:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0.0103)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(110 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0 * const)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(1 * const)
                elif t >= 60 and t < 120:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0.013 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(90 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0 * const)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.6 * const)
                else:
                    self.window.ui.dck_treat_controls.slider[0].setValue(0.0103 * const)  # Parenteral feeding
                    self.window.ui.dck_treat_controls.slider[1].setValue(75 * const)  # Exogenic insulin supply
                    self.window.ui.dck_treat_controls.slider[2].setValue(0)  # Enteral tube feeding
                    self.window.ui.dck_treat_controls.slider[3].setValue(0.6 * const)  # Insulin sensitivity


    def handler_update_graph(self):
        # Update the index and time counters
        self.window.update_time_index()

        # Check end of X axis and append new points
        if self.window.is_index_end_axis():
            self.window.append_new_axis_points()

        #self.change_treatment(99,"a",self.window.indexGr -1 )

        # Update graphs with new points,
        # old points are needed to update the legends
        self.window.update_graph(self.model.getPoint())

    def handler_change_simulated_value(self, i, value):
        self.window.all_data[i][self.window.indexGr] = value
        self.window.all_curves[i].setData(self.window.xDataGraf[:self.window.indexGr + 1], self.window.all_data[i])

        _i = 0
        for eq in self.model._e:
            if self.window.simulated_eq[_i]:
                self.window.leyend.removeItem(eq.name + ': ' + str(round(self.window.dats[_i], self.window.round)) + ' ' + eq.unit)
            _i += 1

        self.window.dats[i] = value #/ self.model.eq_convert_factors[i]
        self.model.change_val(i, value / self.eq_convert_factors[i])
        self.model.recalculate(self.window.step)

        _i = 0
        for eq in self.model._e:
            if self.window.simulated_eq[_i]:
                self.window.leyend.addItem(self.window.all_curves[_i], eq.name + ': ' + str(round(self.window.dats[_i], self.window.round)) + ' ' + eq.unit)

            _i += 1

    def handler_restart_graph(self):
        try:
            self.window.timer.stop()
            self.handler_open_model(self.window.modelUbic)
        except Exception as e:
            print(e)

    def handler_open_model(self, name):
        try:
            if name != "":
                if name.endswith(".xml"):
                    self.window.restart_graphs()

                    self.model = Model()
                    self.model.initialize(name, self.window.step)

                    self.eq_convert_factors = []
                    self.tr_convert_factors = []
                    for eq in self.model._e:
                        self.eq_convert_factors.append(eq.convertFactor)

                    for u in self.model._u:
                        if u.graphAsTreatment:
                            self.tr_convert_factors.append(u.convertFactor)

                    self.window.initialize_graphs(name)

        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def handler_change_language_model(self,language):
        try:
            self.window.restart_graphs()
            self.model = Model()
            self.model.language = language
            self.model.initialize(self.window.modelUbic, self.window.step)
            self.window.initialize_graphs(self.window.modelUbic)
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()



    def handler_definite_controls(self):
        _i = 1
        sliderF = ""
        for userDef in self.model._u:
            if userDef.isSlider:
                sliderF, sl_met_reg, sl_met_nom = self.model.code.definiteSlider(userDef, _i, self.tr_convert_factors[_i-1])

                exec(sliderF)
                exec(sl_met_reg)

                # TODO que entre cuando se suelta el slider o poner un boton
                self.window.ui.dck_treat_controls.slider[_i - 1].valueChanged.connect(eval(sl_met_nom))
                _i += 1

    def create_X_axis(self, init, end, steps):
        return self.model.np.linspace(init, end, steps)

    def handler_step_change(self):
        self.window.step = int(self.window.spboxStep.value())
        self.model.change_scale(self.window.step, self.window.indexGr)
        self.model.recalculate(self.window.step)
        linX = self.model.np.linspace(self.window.xDataGraf[self.window.indexGr]
                        , self.window.xDataGraf[self.window.indexGr] + (self.window.step * ((self.window.simulated_cicle_number * self.window.simulated_cicle_steps) - 1))
                        , self.window.simulated_cicle_number * self.window.simulated_cicle_steps)
        #self.model.np.concatenate((arr1, arr2), axis=0)
        self.window.xDataGraf = self.model.np.append(self.window.xDataGraf[:self.window.indexGr], linX)

        print("Main ", self.window.xDataGraf[:self.window.indexGr +10])

    def handler_change_model_propertie(self, param, changes):
        for param, change, data in changes:
            _i = -1
            var = 1
            if param.name() == 'Simulated':
                print("change simulated")
                while (var):
                    _i += 1
                    if self.model._e[_i].description in param._parent.name():
                        var = 0


                self.window.simulated_eq[_i] = data

                if data:
                    self.window.all_curves[_i] = self.window.create_curve(_i, self.model._e[_i].name)
                    self.window.all_curves[_i].setData(self.window.xDataGraf[:self.window.indexGr + 1],
                                                       self.window.all_data[_i])
                else:
                    self.window.all_curves[_i].clear()

            elif param.name() == 'Color':
                print("change color")
                while (var):
                    _i += 1
                    if self.model._e[_i].description in param._parent.name():
                        var = 0
                self.handler_change_graph_color(_i, "SIMULATION", data)

    def handler_change_graph_color(self, _i, wich, data):
        if wich == "SIMULATION":
            self.window.all_curves[_i].clear()
            if str(data)[0] == '#':
                self.window.ui.dck_model_param_properties.colors[_i] = str(data)
            else:
                self.window.ui.dck_model_param_properties.colors[_i] = str(data.name())
            self.window.all_curves[_i] = self.window.create_curve(_i, self.model._e[_i].name)
            self.window.all_curves[_i].setData(self.window.xDataGraf[:self.window.indexGr + 1], self.window.all_data[_i])
        elif wich == "TREAT":
            self.window.all_treat_curves[_i].clear()
            self.window.all_treat_curves[_i] = self.window.create_treat_curve(_i, self.model._u[_i].name)
            self.window.all_treat_curves[_i].setData(self.window.xDataGraf[:self.window.indexGr + 1],
                                               self.window.treatment[_i])
