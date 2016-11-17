# -*- coding: utf8 -*-
import re,os ,random

from time import gmtime, strftime



class extract :
 folder_Collect = ''
 folder_log = ''
 folder = ''
 THRESHOLD = 10
 UDATE_MODEL = True 
 OVER_WRITE = False
 ScanFromLastest_MODEL = True

 def __init__(self,folder_Source,folder_Article,folder_Log,UPDATE_MODEL,THRESHOLD):
  self.folder_Collect = folder_Source
  self.folder_log =  folder_Log
  self.folder =folder_Article
  self.UPDATE_MODEL = UPDATE_MODEL
  self.THRESHOLD = THRESHOLD 
  
  self.checkDir(self.folder)
  self.checkDir(self.folder_log)   
  
 def Log(self,msg):
  error = open(self.folder_log+'\\ERROR_parser.log','a')
  str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())    
  error.write(str_time+'\n'+msg+'\n\n')
  error.flush()
  error.close()
 
  
 def sorted_ls(self,path):
     mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
     return list(sorted(os.listdir(path), key=mtime ,reverse=self.ScanFromLastest_MODEL))
 
 def checkDir(self,path) : 
  if not os.path.exists(path):
   os.mkdir(path)
 
 def sorted_ls(self,path):
     mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
     return list(sorted(os.listdir(path), key=mtime ,reverse=True))
 
 def reduceSymbol(self,sring):
    list_Symbol = ['<','>','?','"','\'','\\','/',':','|']
    for s in list_Symbol: 
       sring = sring.replace(s,'') 
    return sring
 
 def removeSeq(self,string):
  list_Sequence = ['\n','\r','\t']
  for s in list_Sequence: 
    string = string.replace(s,'') 
  return string   
     
 
 def removeTag(self,Page):
  new_Page = re.sub("<[^>]*>",'', Page)
  new_Page = re.sub('&#[0-9]*;','',new_Page)
  list_Symbol = ['&nbsp;','&hellip;','\n','\r','\t','&amp;','&gt;','&lt;','&mdash;','&rsquo;','  ']
  for s in list_Symbol:
    new_Page = new_Page.replace(s,'') 
  
  return new_Page
 
 def removeAD(self,Page):
  new_Page = re.sub("<a[^>]*>(.*)</a>",'', Page)
  
  return new_Page
 
 def getTitle(self,path,Page): 
   try:
     match = re.search(r'<h2 class="title clearfix" itemprop="headline">(.*?)</h2>',Page,re.S) 
     if match :
       Title = match.group(1)
       Title = self.reduceSymbol((Title)).strip()
       
       return Title
     elif re.search(r'<h2 class="title.*">(.*?)</h2>',Page,re.S):
       match  = re.search(r'<h2 class="title">(.*?)</h2>',Page,re.S)
       Title = match.group(1)
       Title = self.reduceSymbol((Title)).strip()
       return Title  
     else : 
       self.Log(path+'--> getTitle : not match.')
       return None 
   except Exception, e: 
    print '>>getTitle : '+str(e)
    Log('>>getTitle Except :'+str(e))
    return None
  
 def getCategory(self,Page):
   try:
    li = re.search(r'<div class="menu_bread_crumb">(.*?)</div>',Page,re.S)
    if li : 
     match = re.search(r'<em>(.*?)</em>',li.group(1),re.S)
     if match :
       Category = match.group(1)
       Category = self.removeSeq((Category)).strip()
       #print Category
       return Category
     else:
       print '>>getCategory : not match.'
       print Page
       return '其他'
    return '其他'   
   except Exception, e: 
    print '>>getCategory : '+str(e)     
    return '其他'
  
 
 def getContent(self,Page): 
    match_content = re.search(r'<div class="story">(.*?)</div>',Page,re.S)
    if match_content :
      content = match_content.group(1)
      content = self.removeAD(content)
      content = self.removeTag(content).strip()
       
      return content
    else:
      print '>>GetContent : not match '  
      return None

 def run(self):
    
  count_THRESHOLD = 1
  
  if os.path.exists(self.folder_Collect):
   if os.listdir(self.folder_Collect) :
     
     list_year  =  map(int,os.listdir(self.folder_Collect))
     list_year = sorted(list_year,reverse=(  self.ScanFromLastest_MODEL))
     for year in list_year:
      
      path_yearfolder = self.folder_Collect+'\\'+str(year)
      if os.listdir(path_yearfolder):
       list_month = map(int,os.listdir(path_yearfolder))
       list_month = sorted(list_month,reverse=(self.ScanFromLastest_MODEL))
        
       for month in list_month:
        BREAK = False     
        path_monthfolder = path_yearfolder+'\\'+str(month)
        list_news = os.listdir(path_monthfolder)
        print year,month
        if list_news :
         for title in list_news :
          try:     
           path = path_monthfolder+'\\'+title
           if os.path.exists(path):
            Page = open(path).read()
             
            Category = self.getCategory(Page)
            Title = self.getTitle(path,Page)
            if Title is None:
              continue  
            path_category = (self.folder+Category+'\\')
            self.checkDir(path_category.decode('utf8'))
            path_category = path_category  
            
            path_news = (path_category+Title) 
            if os.path.exists(path_news.decode('utf8')) :
              print 'ETTODAY: Extract File exists.',title #,count_THRESHOLD
              if self.UDATE_MODEL == True :
                 count_THRESHOLD += 1
                 if count_THRESHOLD > self.THRESHOLD :
                   BREAK = True
                   break
                 else:
                   continue  
              if not self.OVER_WRITE : 
                 continue 
            Content = self.getContent(Page)
            if Content is None:
              self.Log(path+' content is none')
              continue
            #print list(path_news)  
            news = open(path_news.decode('utf8'),'w')
            news.write(Content)
            news.flush()
            news.close()
            print 'ETTODAY: Extract --> '+title
          except Exception ,e :
            print str(e) 
            self.Log(path+':\n'+str(e))
            continue
       
       
    
      
         
   else:
    print 'Not found year folder'   
  else:
   print 'There are not files that could be analyzed.'  
   
if __name__ == '__main__':
   p = extract('Source\\','Article\\','Log\\',True)
   p.run()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  
