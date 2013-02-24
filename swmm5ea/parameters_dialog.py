from PyQt4 import QtCore, QtGui
import guiqwt.plot

import parameters_dialog_
import swmm_ea_controller

 


class Ui_parameters_dialog(QtGui.QDialog,parameters_dialog_.Ui_Dialog):
    
    def __init__(self):
        super(QtGui.QDialog, self).__init__() # because of multiple inheritance, here we call the __init__ of  QtGui.QDialog
                #first        
        self.setupUi(self)
        self.Number_of_input_init()
        # add choices to swmmp_1 combobox
        self.add_choices()

    
    def add_choices(self):
      
        self.swmmp_1.clear()
        self.swmmp_1.addItems(swmm_ea_controller.SWMMCHOICES)        

    def Number_of_input_init(self):
        self.value_widgets=[]
        self.value_widgets.append([self.vlabel1, self.v_value_1, self.v_value_2])        
        self.on_num_inputs_valueChanged()
    
    @QtCore.pyqtSignature("")
    def on_copyButton_clicked(self):
        for i in range(1,len(self.value_widgets)):
                    for j in range(1,3):        
                        self.value_widgets[i][j].setText(self.value_widgets[0][j].text())
    @QtCore.pyqtSignature("int")
    def on_num_inputs_valueChanged(self,value=1):
        #print "fire!"
        for i in range(1,len(self.value_widgets)):
            for j in range(3):
                self.gridLayout_3.removeWidget(self.value_widgets[i][j])
                self.value_widgets[i][j].setParent(None)
        self.value_widgets=self.value_widgets[0:1]
        for i in range(1,self.number_of_inputs()):
            self.value_widgets.append([QtGui.QLabel(self.scrollAreaWidgetContents), 
                                       QtGui.QLineEdit(self.scrollAreaWidgetContents), 
                                       QtGui.QLineEdit(self.scrollAreaWidgetContents)])
            self.value_widgets[i][0].setText(self.translate("v"+str(i+1)))
            self.value_widgets[i][1].setText(self.v_value_1.text())
            self.value_widgets[i][2].setText(self.v_value_2.text())
            for j in range(3):
                self.gridLayout_3.addWidget(self.value_widgets[i][j], i+1, j, 1, 1)

    @QtCore.pyqtSignature("int")
    def on_swmmp_1_currentIndexChanged (self, index=0):
        en1=(index==swmm_ea_controller.SWMMREULTSTYPE_FLOOD) 
        en2=(index==swmm_ea_controller.SWMMREULTSTYPE_STAGE)
        en=en1 or en2
        self.Cost_function_1.setEnabled(en)
        self.Cost_function_2.setEnabled(en)
        self.maximize.setEnabled(en)
        self.minimize_button.setEnabled(en)
        en=en2
        self.stage_size.setEnabled(en)
        self.discount_rate.setEnabled(en)
        self.stages.setEnabled(en)
            
        
    def getDataMap(self):
        params={}
        params["num_inputs"]= self.num_inputs.value()
        params["maximize"]= self.maximize.isChecked()
        params["pop_size"]=self.pop_size.value()
        params["num_elites"]=self.num_elites.value()
        params["crossover_rate"]=self.Crossover_rate.value()
        params["mutation_rate"]=self.mutation_rate.value()
        params["max_evaluations"]=int(self.num_evaluations.text())
        params["cost_function"]=unicode(self.Cost_function_1.document().toPlainText())
        params["swmmout_cost_function"]=unicode(self.Cost_function_2.document().toPlainText())
        params["stage_size"]=int(self.stage_size.text())
        params["discount_rate"]=float(self.discount_rate.text())
        params["stages"]=self.stages.value()
        params["multiObjective"]=self.multiObjective.isChecked()
        v=self.swmmp_1.currentIndex()
        if v==swmm_ea_controller.SWMMREULTSTYPE_CALIB:
            #SWMMCHOICES calibration
            params["swmmResultCodes"]=[0,0,0] # wel'll have to change this stage in the run. 
        else:
            #SWMMCHOICES 'Flood Volume as a cost', 'Staged Calc. with Flood vol. as cost'
            params["swmmResultCodes"]=[3,0,10]
        params["swmmouttype"]=[v, swmm_ea_controller.SWMMCHOICES[v]]            

        params["valuerange"]=map(lambda x: [float(x[1].text()),float(x[2].text())],self.value_widgets)
        params["num_cpus"]=self.Number_of_cpus.value()
        return params
    
    def setDataMap(self, params_):
        params=params_.__dict__
        self.num_inputs.setValue(params["num_inputs"])
        self.maximize.setChecked(params["maximize"])
        self.pop_size.setValue(params["pop_size"])
        self.num_elites.setValue(params["num_elites"])
        self.Crossover_rate.setValue(float(params["crossover_rate"]))
        self.mutation_rate.setValue(float(params["mutation_rate"]))
        self.num_evaluations.setText(str(params["max_evaluations"]))        
        self.Cost_function_1.insertPlainText(QtCore.QString(params["cost_function"]))
        self.Cost_function_2.insertPlainText(QtCore.QString(params["swmmout_cost_function"]))
        self.discount_rate.setValue(float(params["discount_rate"]))
        self.stage_size.setValue(float(params["stage_size"]))
        self.stages.setValue(int(params["stages"]))
        self.multiObjective.setChecked(params["multiObjective"])
        try:
            if params["swmmouttype"][0]==swmm_ea_controller.SWMMREULTSTYPE_FLOOD:
                #SWMMCHOICES flood volume
                self.swmmp_1.setCurrentIndex(swmm_ea_controller.SWMMREULTSTYPE_FLOOD)
            elif params["swmmouttype"][0]==swmm_ea_controller.SWMMREULTSTYPE_CALIB:
                #SWMMCHOICES calibration
                self.swmmp_1.setCurrentIndex(swmm_ea_controller.SWMMREULTSTYPE_CALIB)
            elif params["swmmouttype"][0]==swmm_ea_controller.SWMMREULTSTYPE_STAGE:
                self.swmmp_1.setCurrentIndex(swmm_ea_controller.SWMMREULTSTYPE_STAGE)
            else:
                raise
        except:
            print "Problem : 'swmmouttype'"
            import sys
            sys.stderr.write("Problem : 'swmmouttype'")
            
        for ct in range(min(len(self.value_widgets), len(params["valuerange"]))):
            self.value_widgets[ct][1].setText(unicode(params["valuerange"][ct][0]))
            self.value_widgets[ct][2].setText(unicode(params["valuerange"][ct][1]))
        self.Number_of_cpus.setValue(int(params["num_cpus"]))
            
    def number_of_inputs(self):
        try:
            n=int(self.num_inputs.value())
            if n < 1 : 
                raise Exception("Value Error") 
        except:
            self.num_inputs.setvalue(self.translate('5'))
            n=5
        return n
    def translate(self,name):
        return QtGui.QApplication.translate("Dialog", name, None, QtGui.QApplication.UnicodeUTF8)
            
