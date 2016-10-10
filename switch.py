#coding: utf-8
import os
import sys
import pyinotify

class EventHandler(pyinotify.ProcessEvent): 
    
    def __init__(self, path): 
        super(EventHandler,self).__init__() 
        self.fp = None
        self.offset = 0        
        self.path = os.path.abspath(path)       
     
    def process_IN_CREATE(self, event):       
        if event.pathname == self.path:
            self.fp = open(self.path)              
    
    def process_IN_MODIFY(self, event):
        if event.pathname == self.path:
            if self.fp is None:
                self.fp = open(self.path)                
            if self.fp:
                cursize = os.path.getsize(self.path) 
                block = cursize - self.offset               
                sys.stdout.write(self.fp.read(block))
                self.offset = cursize                        
        
    def process_IN_CLOSE_WRITE(self, event):       
        if event.pathname == self.path:
            if self.fp:                
                self.fp.close()
                self.offset = 0 
                self.fp = None                                 
     
def start_notify(path, mask):   
   wm = pyinotify.WatchManager() 
   notifier = pyinotify.Notifier(wm,EventHandler('test.txt')) 
   wdd = wm.add_watch(path,mask,rec=True) 
   notifier.loop()       
   
def do_notify(): 
    perfdata_path = './'
    mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY |  pyinotify.IN_CLOSE_WRITE
    start_notify(perfdata_path,mask) 
   
if __name__ == '__main__': 
    do_notify()
