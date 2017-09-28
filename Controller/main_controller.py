import imp
import os.path
import sys

import Controller.EdfWriter as edf
from Model import Plot2 as plt2
from Model.LanguageParser import LanguageParser
import types

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


class Controller():
    def __init__(self, window):
        self.model = plt2
        self.window = window
        self.dataFormat = plt2.df
        # Initialize language hash with English as default language
        self.languageSupport = LanguageParser("SystemLanguageSupport.csv","ENG")

    # TODO: mover a utils
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

    def handler_update_graph(self):
        # Update the index and time counters
        self.window.update_time_index()

        # Check end of X axis and append new points
        if self.window.is_index_end_axis():
            self.window.append_new_axis_points()

        # Update graphs with new points,
        # old points are needed to update the legends
        self.window.update_graph(self.window.dats, plt2.getPoint())

    def handler_change_simulated_value(self, i, value):
        self.window.all_data[i][self.window.indexGr] = value
        self.window.all_curves[i].setData(self.window.xDataGraf[:self.window.indexGr + 1], self.window.all_data[i])

        _i = 0
        for eq in plt2._e:
            self.window.leyend.removeItem(eq.name + ': ' + str(round(self.window.dats[_i], self.window.round)))
            _i += 1

        self.window.dats[i] = value
        plt2.recalculate(self.window.step)

        _i = 0
        for eq in plt2._e:
            self.window.leyend.addItem(self.window.all_curves[_i], eq.name + ': ' + str(round(self.window.dats[_i], self.window.round)))

            _i += 1

    def handler_restart_graph(self):
        try:
            self.window.timer.stop()
            self.handler_open_model(self.window.modelUbic)
        except Exception as e:
            print(e)

    def handler_open_model(self, name):
        if name != "":
            if name.endswith(".xml"):
                self.window.restart_graphs()

                #TODO Create_new_model, hacer new Model
                imp.reload(plt2)
                plt2.initialize(name, self.window.step)

                self.window.initialize_graphs(name)

    def handler_definite_controls(self):
        _i = 1
        sliderF = ""
        for userDef in plt2._u:
            if userDef.isSlider:
                sliderF, sl_met_reg, sl_met_nom = self.model.gen.definiteSlider(userDef, _i)

                exec(sliderF)
                exec(sl_met_reg)

                # TODO que entre cuando se suelta el slider o poner un boton
                self.window.ui.dck_model_param_controls.slider[_i - 1].valueChanged.connect(eval(sl_met_nom))
                _i += 1

    def create_X_axis(self, init, end, steps):
        return plt2.np.linspace(init, end, steps, dtype=plt2.np.int32)
    
    def handler_step_change(self):
        self.window.step = int(self.window.spboxStep.value())
        plt2.change_scale(self.window.step, self.window.indexGr)
        plt2.recalculate(self.window.step)
        linX = plt2.np.linspace(self.window.xDataGraf[self.window.indexGr]
                        , self.window.xDataGraf[self.window.indexGr] + (self.window.step * ((self.window.simulated_cicle_number * self.window.simulated_cicle_steps) - 1))
                        , self.window.simulated_cicle_number * self.window.simulated_cicle_steps, dtype=plt2.np.int32)
        #plt2.np.concatenate((arr1, arr2), axis=0)
        self.window.xDataGraf = plt2.np.append(self.window.xDataGraf[:self.window.indexGr], linX)

        print("Main ", self.window.xDataGraf[:self.window.indexGr +10])
        
    def handler_change_model_propertie(self, param, changes):
        for param, change, data in changes:
            _i = -1
            var = 1
            if param.name() == 'Simulated':
                print("change simulated")
                while (var):
                    _i += 1
                    if plt2._e[_i].description in param._parent.name():
                        var = 0

                self.window.simulated_eq[_i] = data

                if data:
                    self.window.all_curves[_i] = self.window.create_curve(_i, plt2._e[_i].name)
                    self.window.all_curves[_i].setData(self.window.xDataGraf[:self.window.indexGr + 1],
                                                       self.window.all_data[_i])
                else:
                    self.window.all_curves[_i].clear()

            elif param.name() == 'Color':
                print("change color")
                while (var):
                    _i += 1
                    if plt2._e[_i].description in param._parent.name():
                        var = 0

                self.window.all_curves[_i].clear()
                if str(data)[0] == '#':
                    self.window.ui.dck_model_param_properties.colors[_i] = str(data)
                else:
                    self.window.ui.dck_model_param_properties.colors[_i] = str(data.name())
                self.window.all_curves[_i] = self.window.create_curve(_i, plt2._e[_i].name)
                self.window.all_curves[_i].setData(self.window.xDataGraf[:self.window.indexGr + 1], self.window.all_data[_i])

    def handler_edf(self, name):
        self.controller.handler_edf(edf.WriteEDF(plt2._sol[:self.indexGr, :], plt2._e, 1 / 60, name))

    def handler_change_model_parameter(self, param, changes):
            print("tree changes:")
            for param, change, data in changes:
                # path = __parTr1.childPath(param)
                # if path is not None:
                #     childName = '.'.join(path)
                # else:
                childName = param.name()
                print('  parameter: %s' % childName)
                print('  change:    %s' % change)
                print('  data:      %s' % str(data))
                print('  ----------')
                print(eval("plt2." + childName))
                print("plt2." + childName + " = " + data + "")
                exec("plt2." + childName + " = " + data + "")
                print(eval("plt2." + childName))
                plt2.recalculate(self.window.step)

    def createParamsUserDef(self):
        # Tree params
        _listChildUsrDef = []
        _params = []
        for userDef in plt2._u:
            # nomC = const.value1 + ' ' + const.operator
            if not userDef.isSlider:
                _childAuxUsrDef = {'name': userDef.name, 'value': userDef.defaultValue, 'type': 'str',
                                   'readonly': False,
                                   'title': userDef.description + " (" + userDef.unit + ") "}#, 'suffix': userDef.unit, 'siPrefix': True}
                _listChildUsrDef.append(_childAuxUsrDef)
        _paramAuxUsrDef = {'name': 'User Defined', 'type': 'group', 'children': _listChildUsrDef, 'expanded': True}
        _params.append(_paramAuxUsrDef)

        return _params

    def createParamsRest(self):
        # Tree params
        _params = []
        _i = 0
        _listChildAuxEq = []
        for const in plt2._e:
            _childAuxEq = []
            # if const.simulate:
            _childAuxEq = {'name': const.description + ' (' + const.name + ')', 'type': 'group', 'expanded': const.simulate, 'children': [
                    {'name': 'Formula', 'type': 'str',
                        'value': const.equation,
                        'readonly': True},
                    {'name': 'Simulated', 'type': 'bool', 'value': const.simulate, 'readonly': False},
                    {'name': 'Color', 'type': 'color', 'value': self.window.ui.dck_model_param_properties.colors[_i], 'readonly': False},
                    #TODO: agregar mas atributos
                    # {'name': 'Line width', 'type': 'int', 'value': self.pen_size[_i], 'readonly': not const.simulate},
                ]}
            # else:
            #     _childAuxEq = {'name': const.description, 'type': 'group' , 'expanded': const.simulate, 'children': [
            #             {'name': 'Formula', 'type': 'str',
            #                 'value': const.name + ' = ' + const.equation,
            #                 'readonly': True},
            #             {'name': 'Simulated', 'type': 'str', 'value': 'No', 'readonly': True},
            #         ]}
            _listChildAuxEq.append(_childAuxEq)
            _i += 1
            # print(const)
        _paramAux = {'name': 'Equations', 'type': 'group', 'children': _listChildAuxEq, 'expanded': True}
        _params.append(_paramAux)

        _listChildAuxFunc = []
        for const in plt2._f:
            _childAuxFunc = {'name': const.name, 'type': 'str', 'value': const.function, 'siPrefix': False,
                             'readonly': True}
            _listChildAuxFunc.append(_childAuxFunc)
            # print(const)
        _paramAux = {'name': 'Functions', 'type': 'group', 'children': _listChildAuxFunc, 'expanded': False}
        _params.append(_paramAux)

        _listChildAuxConst = []
        for const in plt2._c:
            nomC = const.value1
            # nomC = const.value1 + ' ' + const.operator
            _childAuxConst = {'name': nomC, 'type': 'str', 'value': const.value2, 'readonly': True}
            _listChildAuxConst.append(_childAuxConst)
        _paramAuxConst = {'name': 'Constants', 'type': 'group', 'children': _listChildAuxConst, 'expanded': False}
        _params.append(_paramAuxConst)

        return _params

    def definite_equation_change_control(self):
        _i = 0
        for eq in plt2._e:
            controlFunc = "def eqCtrlChangeValue_" + str(_i) + "(self):\n\t" \
                            "#print(self.eqCtrlList[" + str(_i) + "].value())\n\t"\
                            "self.handler_change_simulated_value(" + str(_i) +\
                            ", self.window.ui.dck_model_param_controls.eqCtrlList[" + str(_i) + "].value())\n\t"

            _c_f_aux = "eqCtrlChangeValue_" + str(_i)
            exec(controlFunc)
            exec("self." + _c_f_aux + " = types.MethodType(" + _c_f_aux + ", self)")

            _i += 1

    def changeSystemLanguage(self,language):
        self.languageSupport = LanguageParser("SystemLanguageSupport.csv", "ENG").changeLanguage(language)






