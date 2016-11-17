import urllib,urllib2,os,re
from time import gmtime, strftime

class collect:
 folder = ''
 folder_log = ''
 THRESHOLD = 50
 UPDATE_MODEL = True

 def __init__(self,folder_Source,folder_Log,UPDATE_MODEL,THRESHOLD):
  self.folder = folder_Source
  self.folder_log = folder_Log
  self.UPDATE_MODEL = UPDATE_MODEL
  self.THRESHOLD = THRESHOLD
     
  if not os.path.exists(self.folder):
   os.mkdir(self.folder)
  if not os.path.exists(self.folder_log):
   os.mkdir(self.folder_log) 

 def getID(self):
  if not self.UPDATE_MODEL  and os.listdir(self.folder) : 
   list_dir = os.listdir(self.folder)
   return int(list_dir[-1].replace('.html',''))
   
  else:
   list_uid = list()   
   for idx_classid in range(1,10):   
    Page = self.getPage('http://www.merit-times.com/PageList.aspx?classid='+str(idx_classid))
    list_link = re.findall(r'"NewsPage.aspx[?]Unid=(.*?)"',Page)
    list_uid += list_link
   return max( map(int,list_uid) )
 
 
 def getPage(self,url):
  req = urllib2.Request(url)  
  Page = urllib2.urlopen(req).read()
  return Page


 def run(self):
  idx = self.getID() 
  count_THRESHOLD  = 0    
  while idx > 1 and count_THRESHOLD < self.THRESHOLD: 
   try: 
    fn = str(idx).zfill(6)+".html"
    path_fn = self.folder+fn
    if os.path.exists(path_fn):
      print 'MERIT: File exists '+ fn
      if self.UPDATE_MODEL :
       count_THRESHOLD += 1 
      continue
    else:  
     url = 'http://www.merit-times.com/NewsPage.aspx?unid='  
     Page = self.getPage(url+str(idx)) 
     txt = open(path_fn, "w")
     txt.write(Page)
     txt.flush()
     txt.close()
     print 'MERIT: Download --> '+fn
      
   except Exception ,e:
     print str(e)  
     str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())  
     txt = open(self.folder_log+"ERROR_collect.log", "a")
     txt.write(str_time+'\n'+str(idx)+':'+str(e))
     txt.flush()
     txt.close()
     print 'id='+str(idx)+' is not found.'
      
     continue
   finally :
     idx -= 1

     
if __name__ == '__main__':
   p = collect('Source\\','Log\\')
   p.run() 
 
