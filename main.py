"""
@author:sudhanshu prajapati
"""
#pyqt5 imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
#from PyQt5.QtWidgets import QMainWindow
#from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from PyQt5.uic import loadUiType
#otherLib
import sys
from os import path
import pymysql

'''Importing custom functions'''
# custom file

import time
import traceback
from medicine_add_mod import med_add
from aws_api import aws_api
from search_query_mod import search_query
from capture import capture
import validator
from search_using_practo import med_practo
'''-----------------------------------------------'''

FORM_CLASS,_ = loadUiType(path.join(path.dirname("__file__"),"Main_window.ui"))

class Main_window(QMainWindow,FORM_CLASS):

    #initialize
    def __init__(self,parent=None):
        super(Main_window,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.btn_login.clicked.connect(self.Login)
        self.create_account.clicked.connect(self.Register)
        self.password.returnPressed.connect(self.Login)
        self.connectDB()

        
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

#universal db access
    def connectDB(self):
            global db
            global cur
            db = pymysql.connect(host="localhost",user="root",password="12345",db="user_info")
            cur= db.cursor()
    
#login logic 
    def Login(self):
        try:
            global use
            use= self.user_name.text()
            pas = self.password.text()
            query="SELECT * FROM login_info where Username=%s and Password=%s"
            cur.execute(query,(use,pas))
            if(len(cur.fetchall())>0):
                self.user_name.clear()
                self.password.clear()
                #self.winDB= self.dashboard()
                self.dashboard()
            else:
                self.check_info.setText("Invalid Username/Password")
                self.warningbox("Alert","enter correct details")
        except Exception as e:
            print(e)


#login error message box
    def warningbox(self,title,message):
        self.mess=QtWidgets.QMessageBox()
        self.mess.setWindowTitle(title)
        self.mess.setText(message)
        self.mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.mess.exec_()


#register window opening and clossing handle buttons
    def Register(self):
        self.hide()
        self.reg=loadUi("Registration.ui")
        self.reg.show()
        self.reg.backtomain.clicked.connect(lambda:self.clicklogout(self.reg))
        self.reg.registerbtn.clicked.connect(self.RegisterDB)


#register logic
    def RegisterDB(self):
        try:
            uname = self.reg.user_reg.text()
            email = self.reg.email_reg.text()
            passw = self.reg.pass_reg.text()

            x=validator.validateReg(uname,email)
            if x:
                self.warningbox("Alert",x)
            else:
                if uname!="" and email!="" and passw!="":
                    check_data="SELECT * FROM login_info where Username=%s or Email=%s"
                    cur.execute(check_data,(uname,email))
                    if(len(cur.fetchall())>0):
                        self.warningbox("Alert","UserName or Email Id Already Exist")
                    else:
                        query="INSERT INTO login_info(Username,Email,Password) VALUES('%s','%s','%s')" % (uname,email,passw)
                        print(query)
                        count = cur.execute(query)
                        if(count == 1):
                            self.reg.user_reg.clear()
                            self.reg.email_reg.clear()
                            self.reg.pass_reg.clear()
                            self.reg.register_info.setText("You are Registered Successfully")

                        db.commit()
        except Exception as e:
            print(e)
            self.ui.label2.setText("You are already register")


#dashboard window click and show handle
    def dashboard(self):
        self.hide()
        self.dlg=loadUi("Dashboard.ui")
        self.dlg.show()
        self.dlg.user_dash.setText(str(use))
        try:
            self.mednames=self.user_search_history(use)
            for i in self.mednames:
                self.dlg.listWidget.addItem(i)
        except Exception as e:
            print(e)
        
        self.dlg.logout.clicked.connect(lambda:self.clicklogout(self.dlg))

        self.dlg.search_das.clicked.connect(self.keywordSearch)
        self.dlg.keyword_text.returnPressed.connect(self.keywordSearch)
       
        self.dlg.btbrowse.clicked.connect(self.file_open)
        self.dlg.take_pic.clicked.connect(self.captureIMG)
        


    
#small function for logout
    def clicklogout(self,dlg):
        self.show()
        dlg.hide()


#keywordsearch window handling
    def keywordSearch(self):
        self.word = self.dlg.keyword_text.text()
        if self.word !="":
            
            #self.dlg.hide()
            print(self.word)
            self.dlg.listWidget.addItem(self.word)
            self.dlg.keyword_text.clear()
            self.keyr=loadUi("keyword_search.ui")
            self.keyr.backtodash.clicked.connect(lambda:self.keyr.close())
            self.keyr.keyword_name.setText(self.word)


            #check enterd keyword already in database if not then add it lowering all letter for better result
            self.ids = med_add(self.word,cur,db)
            #print(self.ids)
            self.update_user_search_history(self.ids)
            self.show_medicine(self.ids)


            self.keyr.show()
        else:
            return


    def show_medicine(self,ids):
        try:
            print(ids)
            cur.execute("SELECT * from med_info where med_id=%s",ids)
            self.med_info=cur.fetchone()
            #print(self.med_info)
            #show part
            self.keyr.keyw_databse.setText(str(self.med_info[1]))
            self.keyr.desc_med.setText(str(self.med_info[2]))
            self.keyr.effect_med.setText(str(self.med_info[3]))
            self.keyr.uses_med.setText(str(self.med_info[4]))
            self.keyr.dosage_med.setText(str(self.med_info[5]))
            self.keyr.subs_med.setText(str(self.med_info[6]))
        except :
            pass




    def update_user_search_history(self,med_id):

        try:
            query="INSERT INTO med_search (med_id,User_id) VALUES ('%s','%s')"%(med_id,user_id)
            cur.execute(query)
            db.commit()
            print("updated med Search history",user_id)
        except Exception as e:
            print("Already exist",e)
            return






#get user previous search history

    def user_search_history(self,use):
        try:
            cur.execute("SELECT User_id FROM login_info where Username=%s",(use))
            global user_id
            (user_id,)=cur.fetchone()
            cur.execute("SELECT med_id from med_search where User_id=%s",(user_id))
            p=cur.fetchall()
            mednames=[]
            for i  in p:
                cur.execute("select medName from med_info where med_id=%s",(i[0]))
                (m,)=cur.fetchone()
                mednames.append(m)
            return mednames
        except:
            return None
        return None


#browse handling
    def file_open(self):
        self.name = QFileDialog.getOpenFileName(self, 'Open File','c:\\',"Image files (*.jpg)")
        print(self.name[0])
        
        #print(self.pixmap)
        #self.lbl.setPixmap(self.pixmap.scaled(self.lbl.size()))
        self.scanSearch(self.name[0])


#Scan search window handling
    def scanSearch(self,pathName):
        self.pixmap =QPixmap(pathName)
        self.scans=loadUi("scan_search.ui")
        self.listWords=self.aws_scan(pathName)
        self.scans.graphicsView.setPixmap(self.pixmap.scaled(self.scans.graphicsView.size()))
        self.scans.backtodash.clicked.connect(lambda:self.scans.close())
        for i in self.listWords:
            if len(i)>4:
                self.scans.imgText.addItem(i)
            else:
                self.scans.imgText.addItem("No data")
                print("No Data")
                
        self.scans.show()            
        self.scans.imgText.itemClicked.connect(
                lambda it : self.listWidgetClicked(it))
    @pyqtSlot()
    def listWidgetClicked(self, item):
        

        print('click -> {}'.format(item.text()))
        temp=str(item.text()) 
        self.word=temp
        try:
            self.ids = med_add(self.word,cur,db)
            #print(self.ids)
        except:
            pass
        self.update_user_search_history(self.ids)
        self.show_medicine_scan(self.ids)

    def show_medicine_scan(self,ids):
        try:
            print(ids)
            cur.execute("SELECT * from med_info where med_id=%s",ids)
            self.med_info=cur.fetchone()
            #print(self.med_info)
            #show part
            self.scans.keyw_databse.setText(str(self.med_info[1]))
            self.scans.desc_med.setText(str(self.med_info[2]))
            self.scans.effect_med.setText(str(self.med_info[3]))
            self.scans.uses_med.setText(str(self.med_info[4]))
            self.scans.dosage_med.setText(str(self.med_info[5]))
            self.scans.subs_med.setText(str(self.med_info[6]))
        except :
            pass


    def aws_scan(self,pathName):
        self.list_words=aws_api(pathName)   #giving it to aws function
        #print(self.list_words)
        return self.list_words



#take a picture button handling
    def capture_info(self,title,message):
        self.mess=QtWidgets.QMessageBox()
        self.mess.setWindowTitle(title)
        self.mess.setText(message)
        self.mess.setIcon(QMessageBox.Information)
        self.mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.mess.exec_()

    def captureIMG(self):
        self.capture_info("capture image","Press S  to Save and Q to Quit/Close")
        self.path=capture()
        self.scanSearch(self.path)


    # def progress_fn(self, n):
    #     print("%d%% done" % n)

    def execute_this_fn(self):
        for n in range(0, 5):
            print(n)
        return "Done."
 
    def print_output(self, s):
        print(s)
        
    def thread_complete(self):
        print("THREAD COMPLETE!")
 
    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        #worker.signals.progress.connect(self.progress_fn)
        
        # Execute
        self.threadpool.start(worker) 




class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    #progress = pyqtSignal(int)



class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
        




# initialize the all
def main():
    app=QApplication(sys.argv)
    window=Main_window()
    window.show()
    app.exec()


if __name__=='__main__':
    main()
