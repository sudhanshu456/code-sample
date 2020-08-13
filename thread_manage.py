from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys

from bs4 import BeautifulSoup
import requests

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
    progress = pyqtSignal(int)
    error = pyqtSignal(tuple)
    finished = pyqtSignal()
    result = pyqtSignal(object)
    
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
        self.kwargs['progress_callback'] = self.signals.progress 

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
        finally:
            self.signals.finished.emit()



class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        
        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)
        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)
    
        self.setCentralWidget(w)
    
        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def myfunc(self,progress_callback):
        search_qurey=input("enter your query")
        url_template="https://www.1mg.com/search/all?name="+search_qurey
        print(url_template)
        temp=requests.get(url_template)
        temp.status_code
        soup=BeautifulSoup(temp.content,"html.parser")
        h=soup.find_all('div',class_="style__horizontal-card___1Zwmt")
        try:
            l=[]
            for i in h:
                links = i.findAll('a')
                for a in links:
                    l.append(a['href'])        
            l[0]
            basedir='https://www.1mg.com'
            final_url=basedir+l[0]
            print(final_url)
            detail_page=requests.get(final_url)
            detail=BeautifulSoup(detail_page.content,'html.parser')
            g=[]
            counts=1
            for row in detail.find_all('div',class_='bodyRegular'):
                    print(row.text)
                    g.append(row.text)
                    progress_callback.emit(counts*100/4)
                    counts+=1
            g[0]
            return g[0]
          
        except IndexError:
            h=soup.find_all('div',class_="style__product-box___3oEU6")
            l=[]
            for i in h:
                links = i.findAll('a')
                for a in links:
                    l.append(a['href'])        
            l[0]
            basedir='https://www.1mg.com'
            final_url=basedir+l[0]
            print(final_url)
            detail_page=requests.get(final_url)
            detail=BeautifulSoup(detail_page.content,'html.parser')
            g=[]
            counts=1
            for row in detail.find_all('div',class_='pNormal marginTop-8'):
                    print(row.text)
                    g.append(row.text)
                    progress_callback.emit(counts*100/4)
                    counts+=1

            g[0]
            return g[0]

    def thread_complete(self):
        print("THREAD COMPLETE!")
    def progress_fn(self, n):
        print("%d%% done" % n)

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.myfunc) # Any other args, kwargs are passed to the run function
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)


        
app = QApplication([])
window = MainWindow()
app.exec_()
