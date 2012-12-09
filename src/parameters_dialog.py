from PyQt4 import QtCore, QtGui
import guiqwt.plot

import parameters_dialog_

class Ui_parameters_dialog(QtGui.QDialog,parameters_dialog_.Ui_Dialog):
    
    def __init__(self):
        super(QtGui.QDialog, self).__init__() # because of multiple inheritance, here we call the __init__ of  QtGui.QDialog
                #first        
        self.setupUi(self)
        self.Number_of_input_init()

    def Number_of_input_init(self):
        self.value_widgets=[]
        self.value_widgets.append([self.vlabel1, self.v_value_1, self.v_value_2])        
        self.on_num_inputs_valueChanged()
    
    @QtCore.pyqtSignature("")
    def on_copyButton_clicked(self):
        for i in range(1,len(self.value_widgets)):
                    for j in range(3):        
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
        params["swmmResultCodes"]=[self.swmmp_1.value(),self.swmmp_2.value(),self.swmmp_3.value()]
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
        self.swmmp_1.setValue(int(params["swmmResultCodes"][0]))
        self.swmmp_2.setValue(int(params["swmmResultCodes"][1]))
        self.swmmp_3.setValue(int(params["swmmResultCodes"][2]))
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
            
if __name__ == "__main__":
    import sys
    params={"crossover_rate" : 0.1 ,"swmmResultCodes" : [2, 3, 4] ,
          "num_inputs" : 5 ,"cost_function" : "v1*2+v2"  ,"mutation_rate" : 0.1 ,
          "num_elites" : 0 ,"maximize" : True ,
          "pop_size" : 0 ,"swmmout_cost_function" : "f*.1" ,"max_evaluations" : 100 ,
          "valuerange" : [[0.1, 250.0], [2.0, 30.0], [0.0, 2500.0], [0.0, 2500.0], [4.0, 20.0]] }
    app = QtGui.QApplication(sys.argv)
    ui = Ui_parameters_dialog()
    ui.setDataMap(params)
    ui.show()
    app.exec_()
    for k,v in ui.getDataMap().iteritems():
        print "\""+k+"\" :",v ,","
    if( params==ui.getDataMap()):
        print "Values Same!"
    else:
        print "VALUES CHNANGED"