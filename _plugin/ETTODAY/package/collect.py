# -*- coding: utf8 -*-

import time
import re
import urllib,urllib2,os
from time import gmtime, strftime


class collect :
 folder = ''
 folder_log = ''
 UPDATE_MODEL = True
 THRESHOLD = 10 
 def __init__(self,Source,Log,UPDATE_MODEL,   THRESHOLD):
  self.folder = Source
  self.folder_log = Log
  self.UPDATE_MODEL = UPDATE_MODEL
 
  self.THRESHOLD = THRESHOLD

 def checkDir(self,path) :
  if not os.path.exists(path):
   os.mkdir(path)
  
 def getMaxPageNum(self,Page): 
    match_number = re.search(r'<p class="info">(.*?)</p>',Page,re.S)
    if match_number :
     try:   
      tmp = match_number.group(1)
      num  = tmp.split('|')[1].split('(')[0].replace('共','').replace('頁','')
      return int(num)
     except:
      return None   
    else:
      #print '>>getMaxPageNum : not match '  
      return None
     
 def reduceSymbol(self,sring):
    list_Symbol = ['<','>','?','"','\'','/',':']
    for s in list_Symbol:
      sring = sring.replace(s,'')
    return sring   
 
 def getTitle(self,info):
    match_title = re.findall(r'<a[^>]*>(.*?)</a>',info)
    if match_title :
     title = re.sub("<[^>]*>",'', match_title[0])
     title = self.reduceSymbol(title).strip()
     return title
    else:
     return None 
 
 def getLink(self,info): 
    match_link = re.findall(r'href="(.*?)"',info)
    if match_link : 
     link =  match_link[0].strip()
     return link
    else:
     return None
 
 def getList_LinkInfo(self,Page):
    list_linkinfo = list() 
    list_info = re.findall(r'<h3 >(.*?)</h3>',Page)
    for info in list_info: 
      title = self.getTitle(info)
      link = self.getLink(info)
      
      if None is not link and None is not title :     
       list_linkinfo.append([title,link])
    return list_linkinfo   

 def getPage(self,url):
  req = urllib2.Request(url)  
  Page = urllib2.urlopen(req).read()
  return Page

 def run(self):
  daysOfMonth = {'1':31,'2':28, '3':31, '4':30, '5':31, '6':30, '7':31, '8':31, '9':30, '10':31, '11':30, '12':31 }
  year_today = int(time.strftime("%Y"))
  month_today = int(time.strftime("%m"))
  day_today = int(time.strftime("%d"))
  self.checkDir(self.folder)
  self.checkDir(self.folder_log)
  
  end_year = 2012
  end_month = 1
  end_day = 1
  
  start_year = year_today
  count_THRESHHOLD = 1
 
  if os.listdir(self.folder) and self.UPDATE_MODEL is False:
    start_year =  min(map(int,os.listdir(self.folder))) 
 
  BREAK = False
 
  for year in range(start_year,end_year-1,-1):
   if BREAK :
        break    
   path_yearFolder = self.folder+'\\'+str(year)
   self.checkDir(path_yearFolder)
 
  
   if year == year_today:
    start_month =  month_today
   else:
    start_month = 12   
   if os.listdir(path_yearFolder) and self.UPDATE_MODEL is False   :
     start_month =  min(map(int,os.listdir(path_yearFolder)))
     
   for month in range(start_month,end_month-1,-1):
    if BREAK :
        break    
    self.checkDir(self.folder+'\\'+str(year)+'\\'+str(month)+'\\')   
    start_day =  daysOfMonth[str(month)]
    if year == year_today and month == month_today:
      start_day = day_today  
    for day in range(start_day,end_day-1,-1):
      if BREAK :
        break  
      count_page = 1
      while count_page    and not BREAK :
       url = 'http://www.ettoday.net/news/news-list-'+str(year)+'-'+str(month)+'-'+str(day)+'-0-'+str(count_page)+'.htm'
       try:
         Page = self.getPage(url)
         MaxPageNum = self.getMaxPageNum(Page)
         print '\n',str(year)+'-'+str(month)+'-'+str(day),'page:'+str(count_page) ,'max_page:'+str(MaxPageNum)
         list_linkinfo = self.getList_LinkInfo(Page)
         for title,link in list_linkinfo: 
           if BREAK:
             break  
           path_year = self.folder+'\\'+str(year)
           self.checkDir(path_year)
           path_month = path_year+'\\'+str(month)
           self.checkDir(path_month)
           path_news = (path_month+'\\'+title).decode('utf8')
           if os.path.exists(path_news):
             print 'ETTODAY: Download File exists. '+title.decode('utf8')
             if self.UPDATE_MODEL :
               count_THRESHHOLD += 1  
               if count_THRESHHOLD >= self.THRESHOLD :
                  BREAK = True  
                
           else:
             
             page = self.getPage(link)
             news = open(path_news,'w')
             news.write(page)
             news.flush()
             news.close()
             print 'ETTODAY: Download --> '+title.decode('utf8')
           #break
           
         count_page += 1
         if count_page > MaxPageNum :
            break  
       except Exception ,e :
         str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())    
         error = open(self.folder_log+'\\ERROR_collector.log','a')
         msg = str(year)+'-'+str(month)+'-'+str(day)+':'+str(e)+'\n\n'
         error.write(str_time+'\n'+msg)
         error.flush()
         error.close()  
         
         count_page += 1
 
 
      
if __name__ == '__main__':
 C = collect('Source\\','Log\\',False)
 C.run()
