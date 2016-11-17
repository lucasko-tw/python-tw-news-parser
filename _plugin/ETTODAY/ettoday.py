
from package.collect import *
from package.extract import *

class ettoday():
 websiteName = 'ETTODAY'
 folder_websiteName =  websiteName+'\\'
  
 def __init__(self,Source,Article,Log,UPDATE_MODEL,THRESHOLD):
  self.Source  =  Source + self.folder_websiteName
  self.Article =  Article + self.folder_websiteName
  self.Log = Log + self.folder_websiteName
  self.UPDATE_MODEL = UPDATE_MODEL
  self.THRESHOLD = THRESHOLD
  
  
  self.checkDir(self.Source)
  self.checkDir(self.Article)
  self.checkDir(self.Log)
  
 def checkDir(self,path):
  if not os.path.exists(path):
    os.mkdir(path)  
    
 def collect(self): 
   collect(self.Source,self.Log,self.UPDATE_MODEL,self.THRESHOLD).run()
   print '===== '+self.websiteName+' Download Finished ====='

 def extract(self):
   extract(self.Source,self.Article,self.Log,self.UPDATE_MODEL,self.THRESHOLD).run()  
   print '===== '+self.websiteName+' Extract Finished ====='
