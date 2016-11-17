# -*- coding: utf8 -*-
import re
import urllib,urllib2,os,time
from time import gmtime, strftime
import datetime

class collect:  
  
 
 THRESHOLD = 10
 UPDATE_MODEL = True
 BREAK = False

 def __init__(self,folder_Source,folder_Log,UPDATE_MODEL,THRESHOLD):
  self.folder = folder_Source
  self.folder_log = folder_Log
  self.THRESHOLD = THRESHOLD
  self.UPDATE_MODEL = UPDATE_MODEL
  
  if not os.path.exists(self.folder):
   os.mkdir(self.folder)
  if not os.path.exists(self.folder_log):
   os.mkdir(self.folder_log)
 
 def getPage(self,url):
  req = urllib2.Request(url)  
  Page = urllib2.urlopen(req).read()
  return Page
 
 def reduceSymbol(self,sring):
    list_Symbol = ['<','>','?','"','\'','\\','/','の',':','*','|']
    for s in list_Symbol:
      sring = sring.replace(s,'')
    return sring
 def checkDate(self,page,time_end):
   time_string = re.findall('<abbr title="(.*?)">',page)[-1] 
   time_news = time_string.split('T')[0] 
   news_datetime = datetime.datetime.strptime(time_news, '%Y-%m-%d').date()
   end_datatime = datetime.datetime.strptime(time_end, '%Y-%m-%d').date()
   if  news_datetime < end_datatime :
     return True
   else:
     return False  

 def run(self): 
  list_type_news = ["politics","finance","stock","industry","economy","real-estate",
   "money-career","international-finance","society","local","taipei",
   "north-taiwan","mid-taiwan","south-taiwan","east-taiwan","entertainment",
   "celebrity","tv-radio","music","movies","jp-kr","sports","baseball",
   "basketball","golf","tennis","other-sports","world","asia-australia",
   "china","america","euro-africa","lifestyle","weather","consumption",
   "travel","transportation","pets","life","pr-news","art-edu","education",
   "art","health","disease","beauty","technology","information-3c","science",
   "travel","odd","comics"]
  
   
  for type_news in list_type_news:
   count = 1
    
   for idx_page  in range(1,40+1): 
     if count > self.THRESHOLD :
       self.BREAK = True
     if self.BREAK :    
       break
     print type_news+',Page:'+str(idx_page)
      
     url_archive = 'http://tw.news.yahoo.com/'+type_news+'/archive/'+str(idx_page)+'.html'
     print url_archive
     page_archive = self.getPage(url_archive)
     url_match = re.findall('<h4><a href="/(.*?)"',page_archive ) 
     for url  in url_match:
       if self.BREAK :    
        break  
       patn_utf8 = (self.folder+'\\'+self.reduceSymbol(url)).decode('utf8')
       if os.path.exists(patn_utf8):
         print 'YAHOO: Downdload file exists. %s'%  (url.decode('utf8'))
         if self.UPDATE_MODEL:
          count += 1
         if count > self.THRESHOLD : 
           break
         else: 
           continue
       elif 'video/' in url :
         continue 
       try :
        
        page = self.getPage('http://tw.news.yahoo.com/'+url)

        
        #self.BREAK = self.checkDate(page,'2014-3-7')
        
        
        
        
        html = open(patn_utf8, "w")
        html.write(page)
        html.flush()
        html.close()
        #news_datetime = datetime.datetime.strptime(time_news, '%y-%m-%d').date()
        print 'YAHOO: Downdload --> '+url.decode('utf8')#,news_datetime
       except Exception,e:
        txt = open(self.folder_log+"\\ERROR_collect.log", "a")
        str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        txt.write(str_time+'\n'+url+':\n'+str(e)+'\n\n')
        txt.flush()
        txt.close()
        print url+' '+str(e)
  
if __name__ == '__main__':
   p = collect('Source\\','Log\\',False,20)
   p.run()
 
